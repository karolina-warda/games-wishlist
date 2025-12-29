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
#game_name = "coral island"
game_names = ["coral island", "pentiment", "Coral islaAd", "firewatch", "soma"]
# with open("./games_list", "r") as file:
#     game_names = [line.strip() for line in file]
#     print(game_names)
for game_name in game_names:
    search_url = f"https://store.playstation.com/en-pl/search/"+game_name 
    driver.get(search_url)
    game_url = driver.find_element(By.XPATH, '//div[@data-qa-index="0"]//div[@data-qa="search#productTile0"]//a[@data-qa=""]').get_attribute("href")
    print(game_url)
    driver.get(game_url)
    time.sleep(2)
    game_title = driver.find_element(By.XPATH, '//h1[@data-qa="mfe-game-title#name"]').text

    try: 
        current_price = driver.find_element(By.XPATH, '//span[@data-qa="mfeCtaMain#offer0#finalPrice"]').text
    except NoSuchElementException: 
        current_price = 'N/A'

    try: 
        final_price = driver.find_element(By.XPATH, '//span[@data-qa="mfeCtaMain#offer1#finalPrice"]').text
    except NoSuchElementException: 
        final_price = 'N/A'

    try: 
        normal_price = driver.find_element(By.XPATH, '//span[@data-qa="mfeCtaMain#offer0#originalPrice"]').text
    except NoSuchElementException: 
        normal_price = 'N/A'

    if current_price == 'Included':
        is_included = 'Yes'
    else: 
        is_included = 'No'

    try: 
        current_price_float = float(current_price.replace("zl", "").replace(",", "."))
    except ValueError:
        current_price_float = 0.00

    try: 
        final_price_float = float(final_price.replace("zl", "").replace(",", "."))
    except ValueError:
        final_price_float = 0.00

    try: 
        normal_price_float = float(normal_price.replace("zl", "").replace(",", "."))
    except ValueError:
        normal_price_float = 0.00

    prices = sorted([current_price_float, final_price_float, normal_price_float])

    if prices[1] != 0.00:
        discount = round(((prices[1]/max(prices)) * 100), 0)
    else: 
        discount = 0

    
    print(game_title, is_included, discount, current_price, final_price, normal_price)

# TODO: add discount expiration date
driver.quit()

