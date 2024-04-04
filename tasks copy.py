import locators
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

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


#image_cv = cv2.imread("output/invoices/1.jpg")
#img_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
#OCR_image_string = pytesseract.image_to_string(img_rgb)
file = open("image_string.txt")
stringi = file.read()
aenean = {"InvoiceDate":r'(?P<InvoiceDate>\d{4}-[01]?\d-[0-3]?\d)',"CompanyName":r'(?P<CompanyName>^[a-z]* LLC)',"InvoiceNo":r'# ?(?P<InvoiceNo>\d*)',"TotalDue":r"^Total:? \D?(?P<TotalDue>\d*[0-9.,]*)$"}
thisdict = {}
for key in aenean:
    thisdict.update(re.search(aenean[key],stringi,flags=re.M|re.I).groupdict())
print(thisdict)
    
file.close()
'''
stringi = open('image_string.txt')

invoice_date = re.finditer(r"^Total:? \D?(?P<TotalDue>\d*[0-9.,]*)$", stringi.read(), flags=re.I | re.M)
stringi.close()

for match in invoice_date:
    print(match.groupdict())


^(?P<Name>.*) +(?P<quantity>\d+) (?P<unitPrice>\d+.\d+) (?P<total>\d+.\d+)?$

(?P<quantity2>\d+) \d+ (\$[0-9.,]+) (\$[0-9.,]+)$

^\S+ +(?P<Name>.+) +(?P<quantity>\d+) +(?P<unitPrice>[0-9.,]+) +(?P<total>[0-9.,]+)?$|^(?P<name>.+) +(?P<quantity2>\d+) +(?P<rate>\$[0-9.,]+) +(?P<amount>\$[0-9.,]+)$

'''