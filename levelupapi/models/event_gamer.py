from django.db.models.deletion import CASCADE
from django.db import models


class Event_Gamer(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)