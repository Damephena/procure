from django.db import models

# from accounts.models import User
# from products.models import Coupon

# Create your models here.
class Session(models.Model):
    data = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SalesOrder(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, to_field='id')
    coupon = models.ForeignKey('products.Coupon', on_delete=models.CASCADE, to_field='id')
    session = models.ForeignKey('Session', on_delete=models.CASCADE, to_field='id')
    order_date = models.DateField()
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    sku = models.CharField(max_length=150) #???
    # order = models.ForeignKey('')
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField(blank=True, default=1)
    subtotal = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

