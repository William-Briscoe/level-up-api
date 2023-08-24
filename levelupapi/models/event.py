from django.db import models


class Event(models.Model):
    date = models.DateField()
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Gamer", through='EventGamer', related_name='attendees')
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name="organizer")
