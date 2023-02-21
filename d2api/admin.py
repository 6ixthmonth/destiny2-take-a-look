from django.contrib import admin

from d2api.models import Item, SalesItem, Vendor

# Register your models here.
admin.site.register([Item, SalesItem, Vendor])
