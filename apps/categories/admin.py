from django.contrib import admin
from .models import Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    list_display_links = ('id', 'name', 'parent')
    search_fields = ('name', 'paarent')
    list_per_page = 10

admin.site.register(Category, CategoryAdmin)

