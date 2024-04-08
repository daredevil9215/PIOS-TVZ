from selenium import webdriver  
import time  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def test_search(query):
    # Open app
    driver.get("http://127.0.0.1:5000/")

    # Find and click "Prijava"
    driver.find_element(By.NAME, "search_query").send_keys(query)

    driver.find_element(By.NAME, "search_query").send_keys(Keys.ENTER)

    time.sleep(3)


if __name__ == "__main__":
    # Chromium options
    chromium_path = '/usr/bin/chromium-browser'
    options = webdriver.ChromeOptions()
    options.binary_location = chromium_path
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    test_search("zagreb")
    test_search("274")

    driver.close()