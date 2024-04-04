import locators
import regexes
import re
import cv2
import pytesseract
import pandas as pd
from robocorp.tasks import task
from RPA.HTTP import HTTP
from datetime import datetime
from robocorp import browser
from bs4 import BeautifulSoup
from io import StringIO
page = browser.page()


@task
def rpa_challenge_invoice_extraction():
    start_the_challenge()
    table = populate_tables()
    download_invoices(table)
    table = scrape_the_invoices(table)
    export_to_csv(table)
    submit_the_csv()
    browser.page().wait_for_timeout(5000)


def start_the_challenge():
    browser.goto(locators.url)
    page.get_by_role(role="button", name="START").click()


def populate_tables():
    page.wait_for_timeout(4000)
    tables = []
    while (True):
        next_button = page.locator(locators.next_btn)
        tables.append(get_one_table())
        if not page.locator(locators.next_enabled).is_visible(timeout=10):
            break
        next_button.click()
    joint_list = pd.concat(tables)
    return joint_list


def get_one_table():
    table_html = page.locator(locators.table).inner_html()
    table = pd.read_html(StringIO(str(table_html)))[0]
    soup_table = BeautifulSoup(
        table_html, 'html.parser').find('table').find_all('tr')
    href_values = []
    for row in soup_table:
        links = row.find_all('a')
        for a in links:
            href = a.get('href')
            href_values.append(href)
    if len(href_values) != len(table['ID']):
        raise ValueError(
            "The amount of links do not match with the amount of lines")

    table['Invoice'] = href_values
    for date in table['Due Date']:
        if not compare_due_date(date):
            row_index = table.index[table['Due Date'] == date]
            table.drop([row_index[0]], inplace=True)
    return table


def compare_due_date(date_string: str):
    today = datetime.today()
    date = datetime.strptime(date_string, '%d-%m-%Y')
    return today >= date


def download_invoices(table):
    http = HTTP()
    for row in table['Invoice']:
        http.download(f"{locators.url}{row}", f'output{row}')


def scrape_the_invoices(Incoming_dataFrame: pd.DataFrame):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    invoice_data_list = []
    for invoice in Incoming_dataFrame['Invoice']:
        image_cv = cv2.imread(f"output{invoice}")
        img_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
        OCR_image_string = pytesseract.image_to_string(img_rgb)

        invoice_variant = identify_invoice_variant(OCR_image_string)
        if invoice_variant is None:
            raise ValueError("Unidentified invoice variant")

        OCR_data = {}
        for key in invoice_variant:
            OCR_data.update(re.search(
                invoice_variant[key], OCR_image_string, flags=re.M | re.I).groupdict())
        format_invoice_date(OCR_data)
        invoice_data_list.append(OCR_data)

    invoice_dataFrame = pd.DataFrame(invoice_data_list)
    combined_dataFrame = pd.concat(
        [Incoming_dataFrame.reset_index(drop=True), invoice_dataFrame], axis=1)
    return combined_dataFrame


def identify_invoice_variant(OCR_image_string):
    identifier = re.search(regexes.variant, OCR_image_string).groupdict()['variant']
    if identifier == 'Aenean':
        return regexes.aenean
    elif identifier == 'INVOICE':
        return regexes.sit_amet
    else:
        raise ValueError("Unrecognized invoice")


def format_invoice_date(OCR_data: dict):
    try:
        OCR_data['InvoiceDate'] = datetime.strptime(
            OCR_data['InvoiceDate'], '%Y-%m-%d')
    except:
        OCR_data['InvoiceDate'] = datetime.strptime(
            OCR_data['InvoiceDate'], '%b %d, %Y')
    OCR_data['InvoiceDate'] = OCR_data['InvoiceDate'].strftime(
        '%d-%m-%Y')


def export_to_csv(table: pd.DataFrame):
    table.drop(['Invoice'], axis=1, inplace=True)
    table.drop(['#'], axis=1, inplace=True)
    table.rename(columns={"Due Date": "DueDate"}, inplace=True)
    table = table[['ID', 'DueDate', 'InvoiceNo',
                   'InvoiceDate', 'CompanyName', 'TotalDue']]
    table.to_csv('tiedosto.csv', index=False)


def submit_the_csv():
    page.locator(locators.submit).set_input_files('tiedosto.csv')
