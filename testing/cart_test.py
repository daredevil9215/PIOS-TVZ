from selenium import webdriver  
import time  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def test_add_to_cart(element_number, quantity):

    print(f'Add to cart test started with order number: {element_number}, quantity: {quantity}')

    try:

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

        print(f'Add to cart test successfully finished with order number: {element_number}, quantity: {quantity}')

    except:

        print(f'Add to cart test failed with order number: {element_number}, quantity: {quantity}')

def test_remove_from_cart(order):

    print(f'Remove from cart test started with order number: {order}')

    try:

        # Open app
        driver.get("http://127.0.0.1:5000/")

        # Find Kosarica tab
        driver.find_element(By.ID, "cart").click()

        # Select Izbrisi button with using the order of ticket
        form = driver.find_element(By.XPATH, "//form[@action='" + "/remove_from_cart/" + str(order) + "']")

        form.click()

        time.sleep(3)

        print(f'Remove from cart test successfully finished with order number: {order}')

    except:

        print(f'Remove from cart test failed with order number: {order}')
    
if __name__ == "__main__":
    # Chromium options
    chromium_path = '/usr/bin/chromium-browser'
    options = webdriver.ChromeOptions()
    options.binary_location = chromium_path
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    test_add_to_cart(element_number=3, quantity=5)
    test_add_to_cart(element_number=5, quantity=10)
    test_remove_from_cart(order=5)

    driver.close()