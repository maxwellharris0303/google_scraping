import requests
import re
from urllib.parse import urljoin

# URL to fetch HTML content from
def available_urls(url):
    # url = "https://www.stanleymartinrenovations.com"
    # url = "https://www.gavi.org"
    pattern = rf"{url}[\w\-\./?=&]+"

    response = requests.get(url)
    html_content = response.text
    # print(html_content)

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


available_urls("https://www.aaremodels.com/")