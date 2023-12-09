from django.db import models

from Device.models import Devices


class Carts(models.Model):
    total = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    device = models.ForeignKey(Devices, on_delete=models.PROTECT, related_name='carts')
