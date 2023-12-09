from django.db import models
from Category.models import Categories


class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    photo = models.CharField(max_length=500)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name='products')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

    def serialize_for_report(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category_id': self.category.id,
            "category_name": self.category.name
        }
