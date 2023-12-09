from django.db import models


class Devices(models.Model):
    name = models.CharField(max_length=100)
    battery = models.IntegerField(default=0)
    locked = models.BooleanField(default=True)
    last_locked_date = models.DateTimeField()
    last_unlocked_date = models.DateTimeField()
