# Source - https://stackoverflow.com/a
# Posted by yuvi, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-04, License - CC BY-SA 3.0

# open file & create csvreader
import csv

# import the relevant model
from gameswishlist.models import GamesList
from django.utils import timezone

CSV_FILE_PATH = "C:/Users/karol/Repos/games-wishlist/games/games_data.csv"

with open(CSV_FILE_PATH, mode ='r') as file:
    csvFile = csv.DictReader(file)
    games_data = [line for line in csvFile] 

#print(games_data)

for line in games_data:

     game = GamesList(searched_title=line["searched_title"], 
                      game_title=line['game_title'],
                      is_included=line["is_included"],
                      discount = line["discount"],
                      discount_expiration = line["discount_expiration"],
                      current_price = line["current_price"],
                      final_price=line["final_price"],
                      normal_price=line["normal_price"],
                      game_url=line["game_url"],
                      image_url=line["image_url"],
                      pub_date = timezone.now())
     try:
         game.save()
     except:
         # if the're a problem anywhere, you wanna know about it
         print(f"there was a problem with line{line}")
