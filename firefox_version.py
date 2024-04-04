from robocorp.tasks import task
from RPA.HTTP import HTTP
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup


@task
def rpa_challenge_invoice_extraction():
    with webdriver.Firefox() as driver:
        start_the_challenge(driver)
        populate_tables(driver)

def start_the_challenge(driver:webdriver.Firefox):
    driver.set_script_timeout(1)
    url = "https://rpachallengeocr.azurewebsites.net/"
    driver.get(url)
    driver.find_element(By.ID,"start").click()    


def populate_tables(driver: webdriver.Firefox):  
    while (True):
        next_nappi = driver.find_element(By.ID, "tableSandbox_next")
      
        if (not driver.find_elements(By.CSS_SELECTOR, ".next.disabled")):
            next_nappi.click()
        else:
            break
    submit_nappi = driver.find_element(By.CSS_SELECTOR, "input[name='csv']")
    submit_nappi.send_keys('\\tiedosto.csv')
    submit_nappi.submit()


   # table[0].to_csv("tiedosto.csv", index=False)
    # from invoice
   # Invoice_number =
   # Invoice_date =
   # Company_name =
   # Total_due =

    # from table
   # Id =
   # Due_date =
