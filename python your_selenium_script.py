from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver (Assuming Chrome, but adjust for your setup)
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=webdriver.ChromeOptions()
)

# Navigate to Google
driver.get("https://www.google.com")

# Ensure the page title is "Google"
assert "Google" in driver.title

# Find the search box element
search_box = driver.find_element("name", "q")

# Type in a search query
search_box.send_keys("Selenium Python")

# Submit the search form
search_box.send_keys(Keys.RETURN)

# Wait for a bit to let the results load
time.sleep(3)

# Check if "Selenium" is in the results
assert "Selenium" in driver.page_source

# Close the browser
driver.quit()
