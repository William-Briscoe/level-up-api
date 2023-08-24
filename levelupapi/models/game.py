from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=50)
    maker = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='maker')
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    num_of_players = models.IntegerField()
    skill_level = models.IntegerField()