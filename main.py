from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import csv

def get_element(url):
    try: 
        element = driver.find_element(By.XPATH, url).text
    except NoSuchElementException: 
        element = 'N/A'
    return element

def cast_float(price):
    try: 
        price_float = float(price.replace("zl", "").replace(",", "."))
    except ValueError:
        price_float = 0.00
    return price_float


# Set up Chrome options (optional)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (optional)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Use a proper Service object
service = Service(ChromeDriverManager().install())


# Initialize driver properly
driver = webdriver.Chrome(service=service, options=options)

games_data_upload = []

with open("/games/games_data.csv", mode ='r') as file:
    csvFile = csv.DictReader(file)
    games_data = [line for line in csvFile] 

for game_data in games_data:
    search_url = f"https://store.playstation.com/en-pl/search/"+game_data["searched_title"]

    if game_data["game_url"] == 'N/A':
        driver.get(search_url)
        game_url = driver.find_element(By.XPATH, '//div[@data-qa-index="0"]//div[@data-qa="search#productTile0"]//a[@data-qa=""]').get_attribute("href")
    else: 
        game_url = game_data["game_url"]

    print(game_url)

    driver.get(game_url)
    time.sleep(2)

    game_title = get_element('//h1[@data-qa="mfe-game-title#name"]')
    current_price = get_element('//span[@data-qa="mfeCtaMain#offer0#finalPrice"]')
    final_price = get_element('//span[@data-qa="mfeCtaMain#offer1#finalPrice"]')
    normal_price = get_element('//span[@data-qa="mfeCtaMain#offer0#originalPrice"]')

    if current_price == 'Included':
        is_included = 'Yes'
    else: 
        is_included = 'No'

    current_price_float = cast_float(current_price)
    final_price_float = cast_float(final_price)
    normal_price_float = cast_float(normal_price)

    prices = sorted([current_price_float, final_price_float, normal_price_float])

    if prices[1] != 0.00:
        discount = 100 - round(((prices[1]/max(prices)) * 100), 0)
    else: 
        discount = 0
    
    if get_element('//span[@data-qa="mfeCtaMain#offer0#discountDescriptor"]') == 'N/A':
        discount_expiration = get_element('//span[@data-qa="mfeCtaMain#offer1#discountDescriptor"]')
    else:
        discount_expiration = get_element('//span[@data-qa="mfeCtaMain#offer0#discountDescriptor"]')
    
    game_dict = {"searched_title":game_data["searched_title"],
                "game_title":game_title, 
                 "is_included":is_included, 
                 "discount":discount, 
                 "discount_expiration":discount_expiration, 
                 "current_price":current_price,
                 "final_price":final_price,
                 "normal_price":normal_price,
                 "game_url":game_url}
    
    games_data_upload.append(game_dict)
    print(game_dict)

df=pd.json_normalize(games_data_upload)
df.to_csv('games_data.csv', encoding='utf-8', index=False)
driver.quit()

