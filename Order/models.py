from django.db import models

from Product.models import Products
from Cart.models import Carts


class Orders(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Products, on_delete=models.PROTECT, related_name='orders')
    amount = models.IntegerField()
    cart = models.ForeignKey(Carts, on_delete=models.PROTECT, related_name='orders')
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def serialize_for_cart(self):
        return {
            'id': self.id,
            'product_name': self.product.name,
            'product_photo': self.product.photo,
            'amount': self.amount,
            'price': self.price
        }
