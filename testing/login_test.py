from selenium import webdriver  
import time  
from selenium.webdriver.common.by import By

def test_user_login(username, password):

    print(f'User login test started with username: {username}, password: {password}')

    try:

        # Open app
        driver.get("http://127.0.0.1:5000/")

        # Find and click "Prijava"
        driver.find_element(By.ID, "prijava").click()

        # Find and input username
        driver.find_element(By.NAME, "username").send_keys(username)

        # Find and input password
        driver.find_element(By.NAME, "password").send_keys(password)

        # Click submit
        driver.find_elements(By.ID, "submit")[0].click()

        print(f'User login test successfully finished with username: {username}, password: {password}')

    except:
        print(f'User login test failed with username: {username}, password: {password}')

def test_logout():
    # Click the logout button
    driver.find_element(By.ID, "odjava").click()


if __name__ == "__main__":
    # Chromium options
    chromium_path = '/usr/bin/chromium-browser'
    options = webdriver.ChromeOptions()
    options.binary_location = chromium_path
    driver = webdriver.Chrome(options=options)

    test_user_login("asd", "asd")
    test_logout()
    test_user_login("admin1", "admin")

    driver.close()