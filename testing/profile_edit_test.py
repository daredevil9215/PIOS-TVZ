from selenium import webdriver  
import time  
from selenium.webdriver.common.by import By

def test_user_balance_change(username, password, balance):
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

    # Click Moj Profil
    driver.find_element(By.ID, "profil").click()

    # Click Uredi Profil
    driver.find_element(By.ID, "edit_profile").click()

    # Change Balance
    driver.find_element(By.ID, "balance").clear()
    driver.find_element(By.ID, "balance").send_keys(str(balance))

    # Submit changes
    driver.find_element(By.ID, "submit").click()

def test_username_change(username, password, new_username):
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

    # Click Moj Profil
    driver.find_element(By.ID, "profil").click()

    # Click Uredi Profil
    driver.find_element(By.ID, "edit_profile").click()

    # Change Username
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys(new_username)

    # Submit changes
    driver.find_element(By.ID, "submit").click()


if __name__ == "__main__":
    # Chromium options
    chromium_path = '/usr/bin/chromium-browser'
    options = webdriver.ChromeOptions()
    options.binary_location = chromium_path
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    test_user_balance_change("ogrg", "grgo", 100)
    #test_username_change("admin1", "admin", "admin2")

    driver.close()