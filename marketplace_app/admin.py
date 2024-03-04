from django.contrib import admin
from .models import Product, Purchase


class ProductDetails(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'image')


class PurchaseDetails(admin.ModelAdmin):
    list_display = ('product', 'seller', 'buyer', 'purchase_price', 'purchase_date')


admin.site.register(Product, ProductDetails)
admin.site.register(Purchase, PurchaseDetails)
