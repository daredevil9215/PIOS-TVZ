from selenium import webdriver  
import time  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def test_user_login(username, password):
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

def test_add_to_cart(element_number, quantity):
    # Open app
    driver.get("http://127.0.0.1:5000/")

    # Find quantity input by element number
    quantity_element = driver.find_element(By.ID, "quantity-" + str(element_number))

    # Increase quantity
    for _ in range(quantity):
        quantity_element.send_keys(Keys.UP)
    
    # Get element by custom HTML attribute
    attribute_name = "data-ticket-id" 
    attribute_value = str(element_number)
    xpath = f"//*[@{attribute_name}='{attribute_value}']"
    click_element = driver.find_element(By.XPATH, xpath)

    time.sleep(1)

    click_element.click()

    time.sleep(1)

def test_order(username, password, payment_method):
    """Available payment methods are: cash and card"""

    # Open app
    driver.get("http://127.0.0.1:5000/")

    test_user_login(username, password)

    test_add_to_cart(5, 5)

    # Find Kosarica tab
    driver.find_element(By.ID, "cart").click()

    # Find Placanje button
    driver.find_element(By.ID, "placanje").click()

    # Select payment method
    driver.find_element(By.ID, payment_method).click()

    # Click Nastavi
    driver.find_element(By.ID, "plati").click()
    
if __name__ == "__main__":
    # Chromium options
    chromium_path = '/usr/bin/chromium-browser'
    options = webdriver.ChromeOptions()
    options.binary_location = chromium_path
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    test_order("ogrg", "grgo", "card")

    driver.close()