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
import contactinfo

FILENAME = 'company_urls.txt'

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
        file.write(data + "\n")


def check_url_validity(url):
    start_time = time.time()

    while time.time() - start_time < 7:
        
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
    time.sleep(3)
    
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
            return data_save("Updated date: " + updated_date[0].strftime("%Y-%m-%d"))
        else:
            return data_save("Updated date: " + updated_date.strftime("%Y-%m-%d"))
    except Exception as e:
        print(f"An error occurred: {e}")
        return data_save("Updated date: None")

driver = webdriver.Chrome()
driver.maximize_window()
# driver.get("https://www.google.com/")

def extract_contact_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Find all phone numbers using regular expression
    phone_numbers = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{10,}[0-9]', soup.get_text())

    # Find all email addresses using regular expression
    email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())
    
    phone_numbers = format_phone_number(phone_numbers)
    email_addresses = remove_duplicates(email_addresses)
    return phone_numbers, email_addresses


def get_contact_info(url):
    phone_numbers = []
    email_addresses = []
    # available_urls = contactinfo.available_urls(url)
    # for u in available_urls:
    #     response = requests.get(u)
    #     html_content = response.text   
    #     phone_numbers, email_addresses = extract_contact_info(html_content)
        
    #     phone_numbers.append(phone_numbers)
    #     email_addresses.append(email_addresses)
    driver1 = webdriver.Chrome()

    # Navigate to the website
    driver1.get(url)
    time.sleep(5)
    # response = requests.get(url)
    # html_content = response.text   
    html_content = driver1.page_source
    driver1.quit()   
    phone_numbers, email_addresses = extract_contact_info(html_content)
    
    if len(phone_numbers) == 0:
        print("No phone number")
        data_save("No phone number")
    if len(email_addresses) == 0:
        print("No email address")
        data_save("No email address")
    if len(phone_numbers) != 0:
        print("Phone Numbers:", phone_numbers)
        data_save(f"Phone Numbers: {phone_numbers}")
    if len(email_addresses) != 0:
        print("Email Addresses:", email_addresses)
        data_save(f"Email Addresses: {email_addresses}")


# driver.get("https://www.google.com/search?q=newly+created+home+improvement+company+usa&sca_esv=572849866&biw=1920&bih=931&tbs=qdr%3Ad&sxsrf=AM9HkKmQBPJWN654y7Xsit1ZmdfXSl1ogA%3A1697198988856&ei=jDMpZcPsM7aVxc8PvZqX4Ao&ved=0ahUKEwjD4t_2_vKBAxW2SvEDHT3NBawQ4dUDCBA&uact=5&oq=newly+created+home+improvement+company+usa&gs_lp=Egxnd3Mtd2l6LXNlcnAiKm5ld2x5IGNyZWF0ZWQgaG9tZSBpbXByb3ZlbWVudCBjb21wYW55IHVzYTIEECMYJzIEECMYJzIEECMYJ0ioB1DeBFjeBHABeAGQAQCYAUqgAUqqAQExuAEDyAEA-AEBwgIKEAAYRxjWBBiwA-IDBBgAIEGIBgGQBgg&sclient=gws-wiz-serp")
# driver.get("https://www.google.com/search?q=Testerup&rlz=1C1GCEB_enDE1078DE1078&oq=Testerup&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORiABDIHCAEQABiABDIGCAIQABgeMgYIAxAAGB4yBggEEAAYHjIGCAUQABgeMgYIBhAAGB4yBggHEAAYHjIGCAgQABgeMgYICRAAGB7SAQgyOTM2ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8")
driver.get("https://www.google.com/search?q=Mistplay&oq=Mistplay&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORiABDIHCAEQABiABDIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIHCAkQABiABNIBBzk1MGowajeoAgCwAgA&sourceid=chrome&ie=UTF-8")

WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id=\"L2AGLb\"]"))).click()

start_time = time.time()

while time.time() - start_time < 10:
    pyautogui.scroll(-1000)
    time.sleep(0.1)

# company_element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class=\"sVXRqc\"]")))
# company_url = company_element.get_attribute('data-pcu')
# print(company_url)



elements = driver.find_elements(By.CSS_SELECTOR, "a[class=\"sVXRqc\"]")
print(len(elements))
for i in elements:
    url = i.get_attribute('data-pcu')
    # url = get_root_url(initial_url)
    valid_url_check = check_url_validity(url)
    existed = check_url_in_file(url)
    if existed == False and valid_url_check == True:
        print(url)
        data_save(url)
        get_contact_info(url)
        get_updated_date(url)
elements1 = driver.find_elements(By.CSS_SELECTOR, "a[jsname=\"UWckNb\"]")
print(len(elements1))
for j in elements1:
    url = j.get_attribute('href')
    # url = get_root_url(initial_url)
    valid_url_check = check_url_validity(url)
    existed = check_url_in_file(url)
    if existed == False and valid_url_check == True:
        print(url)
        data_save(url)
        get_contact_info(url)
        get_updated_date(url)

driver.quit()
