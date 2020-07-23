import uuid
import secrets
from django.db import models
from procure import settings

from accounts.models import Address
from products.models import Coupon, Product


class OrderProduct(models.Model):
    '''
    Model to choose a product and quantity
    '''
    user = user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True)
    ordered = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.user.first_name + ': ' + str(self.product.name)

    def get_item_price(self):
        return self.quantity * (self.product.regular_price - self.product.discount_price)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id')
    ref_code = models.CharField(max_length=250, default=secrets.token_urlsafe(), blank=True, unique=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    order_items = models.ManyToManyField(OrderProduct)
    description = models.TextField(blank=True, null=True, help_text='Name your order. Eg: Urgent purchases')
    ordered = models.BooleanField(default=False, blank=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_ref_code(self):
        return self.ref_code

    # def __str__(self):
    #     self.id

    def get_total(self):
        self.calc = [product.get_item_price() for product in self.order_items.all()]
        return sum(self.calc)
    
    def get_items_quantity(self):
        return sum([product.quantity for product in self.order_items.all()])


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    # order = models.ForeignKey('Order', on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name


class Refund(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return self.email + ': ' + str(self.order.get_total())
