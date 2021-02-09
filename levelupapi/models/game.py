from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=50)
    game_type = models.ForeignKey("Game_Type", on_delete=models.CASCADE)
    number_of_players = models.IntegerField()
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)