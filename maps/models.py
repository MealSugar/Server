from django.db import models


class Map(models.Model):
    map_id = models.BigAutoField(primary_key=True)
    latitude = models.DecimalField(max_digits=23, decimal_places=20)
    longitude = models.DecimalField(max_digits=24, decimal_places=20)
    place_type = models.CharField(max_length=15, blank=True)
    place_name = models.CharField(max_length=20, blank=True)
    place_link = models.URLField(max_length=200, blank=True)
    road_name_address = models.TextField(blank=True)
    lot_number_address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)