import requests

def check_url_validity(url):
    try:
        response = requests.head(url)
        print(response.status_code)
        if response.status_code == 200:
            print("URL is valid and accessible.")
        else:
            print("URL is not valid or not accessible.")
    except requests.exceptions.MissingSchema:
        print("Invalid URL format.")
    except requests.exceptions.ConnectionError:
        print("Failed to establish a connection to the URL.")

check_url_validity("https://www.lowes.com")