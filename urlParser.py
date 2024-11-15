from urllib.parse import urlparse

def get_root_url(url):
    parsed_url = urlparse(url)
    root_url = parsed_url.scheme + "://" + parsed_url.netloc
    return root_url

# Example usage
urls = [
    "https://www.businesswire.com/news/home/20231012328667/en/Blue-Yonder-Highlights-Company-Investments-and-Technology-During-ICON-London-2023",
    "https://mcartmed.ru/c2xii/kenmore-air-conditioner-side-panels.html",
    "https://www.con-telegraph.ie/2023/10/12/mayo-exhibitors-at-the-permanent-tsb-ideal-home-show/"
]

for url in urls:
    root_url = get_root_url(url)
    print(root_url)