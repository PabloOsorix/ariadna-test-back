from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_created', 'category', 'price', 'value', 'stock')
    list_display_links = ('id', 'name')
    list_filter = ('category',)
    list_editable = ('price', 'stock', 'value')
    search_fields = ('name', 'description')
    list_per_page = 25

admin.site.register(Product, ProductAdmin)
