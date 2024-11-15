import re
from urllib.parse import urljoin

# Content containing URLs
content = """
Example Domain

Example Domain
This domain is for use in illustrative examples in documents. You may use this
    domain in literature without prior coordination or asking for permission.
More information...

Visit http://example.com for more details.
Check out https://www.example.com for additional information.
<a href="/contactus/">Contact Us</a>
"""

# Base URL
base_url = "https://www.uschamber.com/"

# Regular expression pattern to match URLs containing "http://example.com"
pattern = r"http://example\.com[\w\-\./\?=&]+"

# Find all URLs matching the pattern
urls = re.findall(pattern, content)

# Remove duplicate URLs using set()
unique_urls = set(urls)

# Process relative URLs and add them to unique_urls
for url in re.findall(r'href="([^"]+)"', content):
    complete_url = urljoin(base_url, url)
    unique_urls.add(complete_url)

# Print the unique URLs
for url in unique_urls:
    print(url)