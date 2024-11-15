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
import getContactUrl
import clearEmail

FILENAME = 'new_company_urls.txt'

def get_root_url(url):
    parsed_url = urlparse(url)
    root_url = parsed_url.scheme + "://" + parsed_url.netloc
    return root_url

def check_url_in_file(url):
    with open(FILENAME, 'r') as file:
        file_content = file.read()
        if url in file_content:
            return True
        else:
            return False

def data_save(data):
    with open(FILENAME, "a") as file:
        file.write(data + "\t")

def data_save_date(data):
    with open(FILENAME, "a") as file:
        file.write(data + "\n")


def check_url_validity(url):
           
    try:
        response = requests.head(url)
        if response.status_code == 200:
            # print("URL is valid and accessible.")
            return True
        else:
            return True
    except requests.exceptions.MissingSchema:
        return False
    except requests.exceptions.ConnectionError:
        return False
    except:
        return False
    
def check_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False
    
def format_phone_number(phone_number):
    # Remove any non-digit characters from the phone number
    array = []
    for num in phone_number:
        digits = ''.join(filter(str.isdigit, num))
        digits = digits[-10:]

        # Check if the phone number has a valid length
        if len(digits) >= 10:
            # Format the phone number in the desired format
            formatted_number = "+1 ({}) {}-{}".format(digits[-10:-7], digits[-7:-4], digits[-4:])
            if check_phone_number(formatted_number) == True:
                array.append(formatted_number)

    array = remove_duplicates(array)

    return array

def remove_duplicates(arr):
    unique_arr = []
    for item in arr:
        if item not in unique_arr:
            unique_arr.append(item)
    return unique_arr

def get_updated_date(url):
    try:
        domain = whois.whois(url)
        updated_date = domain.updated_date
        if isinstance(updated_date, list):
            data_save_date(updated_date[0].strftime("%Y-%m-%d"))
        else:
            data_save_date(updated_date.strftime("%Y-%m-%d"))
    except Exception as e:
        print(f"An error occurred: {e}")
        data_save_date("None")
        pass

driver = webdriver.Chrome()
driver.maximize_window()
# driver.get("https://www.google.com/")

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
    
    phone_numbers = format_phone_number(phone_numbers)
    email_addresses = remove_duplicates(email_addresses)
    return phone_numbers, email_addresses


def get_contact_info(url):
    phoneNumbers = []
    emailAddresses = []
    # url = 'https://www.williamshomes.com'
    # url = 'https://www.mrhandyman.com'
    driver1 = webdriver.Chrome()

    available_urls = getContactUrl.available_urls(url, driver1)
    for u in available_urls:
        driver1.get(u)
        time.sleep(5)
        html_content = driver1.page_source
        phone_numbers, email_addresses = extract_contact_info(html_content)

        phoneNumbers.extend(phone_numbers)
        emailAddresses.extend(email_addresses)
    phoneNumbers = remove_duplicates(phoneNumbers)
    emailAddresses = remove_duplicates(emailAddresses)
    driver1.quit()

    # clear Email to correct Email
    emailAddresses = clearEmail.clear_emails(emailAddresses)
    
    if len(phoneNumbers) == 0:
        print("No phone number")
        data_save("No phone number")
    if len(phoneNumbers) != 0:
        print("Phone Numbers:", phoneNumbers)
        # data_save(f"Phone Numbers: {phoneNumbers}")
        data_save(f"{phoneNumbers}")
    if len(emailAddresses) == 0:
        print("No email address")
        data_save("No email address")
    if len(emailAddresses) != 0:
        print("Email Addresses:", emailAddresses)
        # data_save(f"Email Addresses: {emailAddresses}")
        data_save(f"{emailAddresses}")



# driver.get("https://www.google.com/search?q=newly+created+home+improvement+company+usa&sca_esv=572849866&biw=1920&bih=931&tbs=qdr%3Ad&sxsrf=AM9HkKmQBPJWN654y7Xsit1ZmdfXSl1ogA%3A1697198988856&ei=jDMpZcPsM7aVxc8PvZqX4Ao&ved=0ahUKEwjD4t_2_vKBAxW2SvEDHT3NBawQ4dUDCBA&uact=5&oq=newly+created+home+improvement+company+usa&gs_lp=Egxnd3Mtd2l6LXNlcnAiKm5ld2x5IGNyZWF0ZWQgaG9tZSBpbXByb3ZlbWVudCBjb21wYW55IHVzYTIEECMYJzIEECMYJzIEECMYJ0ioB1DeBFjeBHABeAGQAQCYAUqgAUqqAQExuAEDyAEA-AEBwgIKEAAYRxjWBBiwA-IDBBgAIEGIBgGQBgg&sclient=gws-wiz-serp")
driver.get('https://www.google.com/search?q=newly+founded+home+improvement+company+usa&sca_esv=572849866&biw=1920&bih=931&tbs=qdr%3Ad&sxsrf=AM9HkKlv2nhA-dXuQsYmYEwte2mkSqOpzA%3A1697427245377&ei=La8sZYXQFoHkxc8P0dqA6Ak&ved=0ahUKEwjFmvif0fmBAxUBcvEDHVEtAJ0Q4dUDCBA&uact=5&oq=newly+founded+home+improvement+company+usa&gs_lp=Egxnd3Mtd2l6LXNlcnAiKm5ld2x5IGZvdW5kZWQgaG9tZSBpbXByb3ZlbWVudCBjb21wYW55IHVzYTIFEAAYogQyBRAAGKIEMgUQABiiBEjVN1DXB1jNKXADeAGQAQCYAWugAdUEqgEDNi4xuAEDyAEA-AEBwgIKEAAYRxjWBBiwA8ICChAhGKABGMMEGAriAwQYACBBiAYBkAYI&sclient=gws-wiz-serp#ip=1')
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id=\"L2AGLb\"]"))).click()

reached_end_element = False

pyautogui.scroll(-1000)

while(reached_end_element == False):
    time.sleep(0.1)
    try:
        driver.find_element(By.CSS_SELECTOR, "div[class=\"ClPXac Pqkn2e\"")
        reached_end_element = True
    except:
        try:
            driver.find_element(By.CSS_SELECTOR, "div[class=\"GNJvt ipz2Oe\"").click()
            # print("click")
        except:
            pass


elements = driver.find_elements(By.CSS_SELECTOR, "a[class=\"sVXRqc\"]")
print(len(elements))
for i in elements:
    try:
        initial_url = i.get_attribute('data-pcu')
        url = get_root_url(initial_url)
        valid_url_check = check_url_validity(url)
        existed = check_url_in_file(url)
        if existed == False and valid_url_check == True:
            print(url)
            data_save(url)
            get_contact_info(url)
            get_updated_date(url)
    except:
        pass
elements1 = driver.find_elements(By.CSS_SELECTOR, "a[jsname=\"UWckNb\"]")
print(len(elements1))
for j in elements1:
    try:
        initial_url = j.get_attribute('href')
        url = get_root_url(initial_url)
        valid_url_check = check_url_validity(url)
        existed = check_url_in_file(url)
        if existed == False and valid_url_check == True:
            print(url)
            data_save(url)
            get_contact_info(url)
            get_updated_date(url)
    except:
        pass

driver.quit()
