from django.db import models


class Transaction(models.Model):
    code = models.CharField(max_length=250, unique=True) # ???
    order = models.ForeignKey('orders.OrderProduct', models.CASCADE)
