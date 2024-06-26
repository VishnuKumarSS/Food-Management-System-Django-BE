from django.db import models


class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField()
    quantity_sold = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['name']
