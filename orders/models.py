import uuid
from django.db import models

# from accounts.models import User
# from products.models import Coupon

# Create your models here.
# class Session(models.Model):
#     data = models.TextField(max_length=250)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, to_field='id')
    coupon = models.ForeignKey('products.Coupon', on_delete=models.CASCADE, to_field='id', blank=True, null=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, to_field='id')
    unit = models.PositiveIntegerField(default=1, blank=True)
    # session = models.ForeignKey('Session', on_delete=models.CASCADE, to_field='id')
    # order_date = models.DateField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        self.user.first_name + ': ' + str(self.price)


class Cart(models.Model):
    # sku = models.CharField(max_length=150) #???
    # order = models.ForeignKey('')
    # name = models.CharField(max_length=50)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, to_field='id')
    description = models.TextField(blank=True, null=True, help_text='Name your cart. Eg: Urgent purchases')
    orders = models.ManyToManyField(Order)
    items_quantity = models.IntegerField(blank=True, default=1)
    subtotal = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        self.user.first_name + ': ' + str(self.subtotal)
