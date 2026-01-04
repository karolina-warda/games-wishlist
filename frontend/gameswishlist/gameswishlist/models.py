from django.db import models


class GamesList(models.Model):
    searched_title = models.CharField(max_length=200)
    game_title = models.CharField(max_length=200)
    is_included = models.CharField(max_length=10)
    discount= models.CharField(max_length=10)
    discount_expiration= models.CharField(max_length=200)
    current_price= models.CharField(max_length=20)
    final_price= models.CharField(max_length=10)
    normal_price= models.CharField(max_length=10)
    game_url= models.CharField(max_length=200)
    image_url= models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.searched_title
