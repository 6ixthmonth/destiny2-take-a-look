from django.db import models
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    item_hash = models.BigIntegerField(primary_key=True)
    item_name = models.CharField(max_length=255)
    icon_url = models.CharField(max_length=2083)
    character_class = models.CharField(max_length=7)

class Vendor(models.Model):
    vendor_hash = models.BigIntegerField(primary_key=True)
    vendor_name = models.CharField(max_length=255)
    
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
