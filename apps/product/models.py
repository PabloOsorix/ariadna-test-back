from django.db import models
from datetime import datetime
from ..categories.models import Category
# Create your models here.


class Product (models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=datetime.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=3)
    value = models.DecimalField(max_digits=6, decimal_places=3)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
