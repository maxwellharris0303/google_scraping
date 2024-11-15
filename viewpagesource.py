from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the website
driver.get("https://modernrenovations.com/")

# Wait for the splash screen to disappear (assuming it's an element with the ID "splash-screen")

# Wait for an additional 5 seconds to make sure all content is loaded
time.sleep(5)

# Get the HTML content
html_content = driver.page_source

# Close the browser
driver.quit()

# Print the HTML content
print(html_content)