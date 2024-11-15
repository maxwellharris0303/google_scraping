from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re
import time
from urllib.parse import urljoin


# URL to fetch HTML content from
def available_urls(url, driver):
    # url = "https://www.stanleymartinrenovations.com"

    driver.get(url)
    time.sleep(5)
    html_content = driver.page_source

    pattern = rf"{url}[\w\-\./?=&]+"

    urls = re.findall(pattern, html_content)
    # print(urls)
    unique_urls = set(urls)
    unique_urls.add(url)

    # for index_url in re.findall(r'href="([^"]+)"', html_content):
    #     complete_url = urljoin(url, index_url)
    #     unique_urls.add(complete_url)
    for index_url in re.findall(r'href="([^"]+)"', html_content):
        complete_url = urljoin(url, index_url)
        if 'contact' in complete_url:
            unique_urls.add(complete_url)


    # unique_urls = set(urls)
    # print(unique_urls)

    filtered_urls = [
        url for url in unique_urls
        if not re.search(r"\.[a-zA-Z0-9]+$", url) and "contact" in url
    ]
    filtered_urls.append(url)
    print(filtered_urls)
    return filtered_urls

# driver = webdriver.Chrome()
# available_urls("https://www.morningstar.com", driver)