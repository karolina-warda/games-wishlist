from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

element_list = []

# Set up Chrome options (optional)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (optional)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Use a proper Service object
service = Service(ChromeDriverManager().install())


# Initialize driver properly
driver = webdriver.Chrome(service=service, options=options)

# Load the URL
url = f"https://store.playstation.com/en-pl/product/EP3717-PPSA17226_00-CORALISLANDPS5EU"
#url = f"https://store.playstation.com/en-pl/product/EP6311-PPSA16616_00-PLATITUDE0000000"
driver.get(url)
time.sleep(2)  # Optional wait to ensure page loads

# Extract product details


try: 
    is_included = driver.find_element(By.XPATH, '//span[@data-qa="mfeCtaMain#offer0#finalPrice"]').text
except NoSuchElementException: 
    is_included = 'N/A'

try: 
    final_price = driver.find_element(By.XPATH, '//span[@data-qa="mfeCtaMain#offer1#finalPrice"]').text
except NoSuchElementException: 
    final_price = 'N/A'

try: 
    normal_price = driver.find_element(By.XPATH, '//span[@data-qa="mfeCtaMain#offer0#originalPrice"]').text
except NoSuchElementException: 
    normal_price = 'N/A'
    
print(is_included, final_price, normal_price)
driver.quit()

# Display extracted data
# for row in element_list:
#     print(row)