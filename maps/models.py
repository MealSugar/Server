from django.db import models


class Map(models.Model):
    latitude = models.DecimalField(max_digits=23, decimal_places=20)
    longitude = models.DecimalField(max_digits=24, decimal_places=20)
    place_type = models.CharField(max_length=10)