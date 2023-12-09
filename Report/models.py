from django.db import models
from datetime import datetime


class Reports(models.Model):
    date = models.DateTimeField(default=datetime.now())
    device_id = models.BigIntegerField()
    device_name = models.CharField(max_length=100)
    category_id = models.BigIntegerField()
    category_name = models.CharField(max_length=100)
    product_id = models.BigIntegerField()
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(decimal_places=2, max_digits=10)
    order_date = models.DateTimeField(default=datetime.now())
    amount = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)


class CashReports(models.Model):
    date = models.DateTimeField(default=datetime.now())
    device_id = models.BigIntegerField()
    device_name = models.CharField(max_length=100)
    total = models.DecimalField(decimal_places=2, max_digits=10)
