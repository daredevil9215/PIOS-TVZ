from selenium import webdriver  
import time  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_user_register(firstname, lastname, username, email, password):
    # Open app
    driver.get("http://127.0.0.1:5000/")

    # Find "Prijava"
    driver.find_element(By.ID, "prijava").click()

    # Find "Registracija"
    driver.find_element(By.ID, "registracija").click()

    # Enter firstname
    driver.find_element(By.ID, "firstname").send_keys(firstname)

    # Enter lastname
    driver.find_element(By.ID, "lastname").send_keys(lastname)

    # Enter username
    driver.find_element(By.ID, "username").send_keys(username)

    # Enter email
    driver.find_element(By.ID, "email").send_keys(email)

    # Enter password
    driver.find_element(By.ID, "password").send_keys(password)

    # Repeat password
    driver.find_element(By.ID, "password2").send_keys(password)

    # Scroll to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Click register
    driver.find_element(By.ID, "registriraj").click()


if __name__ == "__main__":
    # Chromium options
    chromium_path = '/usr/bin/chromium-browser'
    options = webdriver.ChromeOptions()
    options.binary_location = chromium_path
    driver = webdriver.Chrome(options=options)

    test_user_register("robi", "robi", "robi", "robi@robi.com", "robi")

    driver.close()