from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
import re
import requests
import pyautogui
import time
from urllib.parse import urlparse
import phonenumbers
import whois

FILENAME = 'html_content.txt'

def data_save(data):
    with open(FILENAME, "a") as file:
        file.write(data + "\n")

def extract_contact_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Find all phone numbers using regular expression
    phone_numbers = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{10,}[0-9]', soup.get_text())

    # Find all email addresses using regular expression
    email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())

    tel_links = soup.find_all(href=re.compile(r'tel:'))
    href_phone_numbers = [re.sub(r'tel:', '', link.get('href')) for link in tel_links]

    phone_numbers.extend(href_phone_numbers)

    email_links = soup.find_all(href=re.compile(r'mailto:'))
    href_email = [re.sub(r'mailto:', '', link.get('href')) for link in email_links]

    email_addresses.extend(href_email)
    
    return phone_numbers, email_addresses

url = 'https://www.morningstar.com/company/global-contacts'
driver1 = webdriver.Chrome()

# Navigate to the website
driver1.get(url)
time.sleep(5)
# response = requests.get(url)
# html_content = response.text   
html_content = driver1.page_source
driver1.quit()

print(extract_contact_info(html_content))