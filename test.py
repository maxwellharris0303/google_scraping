from bs4 import BeautifulSoup
import time
import requests
import openai

openai.api_key='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'

def get_urls(keyword):
    search_url = f'https://www.google.com/search?q={keyword}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()

    scroll_iterations = 3
    for _ in range(scroll_iterations):
        time.sleep(2)
        response = requests.get(search_url + '&start=' + str(_ * 10), headers=headers)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    result_divs = soup.find_all('div', class_='yuRUbf')
    urls = []
    for div in result_divs:
        link = div.find('a')
        url = link['href']
        urls.append(url)
        
    return urls

def sumarize(content):
    content = content[:5000]
    prompt = f'Give me main points as three short sentences about following sentences. {content}'
    response = openai.Completion.create(
        engine='davinci',
        prompt=prompt,
        max_tokens=100
    )
    generated_text = response.choices[0].text.strip()
    return generated_text

def get_texts(urls):
    results = []
    for url in urls:
        print(f"Geting data from {url}")
        response = requests.get(url)
        if response.status_code == 200:
            page = response.text
            parsed_page = BeautifulSoup(page, 'html.parser')
            title = parsed_page.find('title').get_text()
            content_tags = parsed_page.find_all(['p', 'h1'])
            content = ' '.join(tag.get_text(strip=True) for tag in content_tags)
            sumarized_content = sumarize(content)
            
            result = {
                'url': url,
                'title': title,
                'content': sumarized_content
            }
            print(result)
            results.append(result)
        else:
            print(f"The site is not responding: {url}")
    return results

keyword = input("Please input keywords: ")
urls = get_urls(keyword)
print(urls)
result = get_texts(urls)
print(result)