from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    num_of_players = models.IntegerField()
    skill_level = models.IntegerField()
    gamer = models.ForeignKey("Gamer", null=True, blank=True, on_delete=models.CASCADE)