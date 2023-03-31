from django.contrib import admin

from d2api.models import Item, SalesItem, Vendor

class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_hash', 'item_name')

class SalesItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_hash', 'vendor_hash', 'sales_date')

class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_hash', 'vendor_name')

# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(SalesItem, SalesItemAdmin)
admin.site.register(Vendor, VendorAdmin)
