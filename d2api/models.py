from django.db import models
from django.utils import timezone


class Item(models.Model):
    item_hash = models.BigIntegerField(primary_key=True)
    item_name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=255)
    class_type = models.PositiveSmallIntegerField(default=0)
    icon_url = models.CharField(max_length=2083)

    def __str__(self) -> str:
        return self.item_name

class Vendor(models.Model):
    vendor_hash = models.BigIntegerField(primary_key=True)
    vendor_name = models.CharField(max_length=255)
    icon_url = models.CharField(max_length=2083)

    def __str__(self) -> str:
        return self.vendor_name
    
class SalesItem(models.Model):
    item_hash = models.ForeignKey(Item, on_delete=models.CASCADE)
    vendor_hash = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    sales_date = models.DateTimeField(default=timezone.now)
    mobility = models.PositiveSmallIntegerField(default=0)
    resilience = models.PositiveSmallIntegerField(default=0)
    recovery = models.PositiveSmallIntegerField(default=0)
    discipline = models.PositiveSmallIntegerField(default=0)
    intellect = models.PositiveSmallIntegerField(default=0)
    strength = models.PositiveSmallIntegerField(default=0)
    pve_recommendation = models.FloatField(default=0.0)
    pvp_recommendation = models.FloatField(default=0.0)
