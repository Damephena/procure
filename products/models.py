import uuid
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=400)
    description = models.TextField(max_length=250)
    active = models.BooleanField(default=False)
    value = models.IntegerField(default=10)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    multiple = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
# An SKU number is a unique code that is assigned to each product in a company's inventory. 
#  SKU stands for "Stock Keeping Unit"
class ProductCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, to_field='id')
    product_sku = models.ForeignKey('Product', on_delete=models.CASCADE, to_field='sku')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductStatus(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductTag(models.Model):
    product_sku = models.ForeignKey('Product', on_delete=models.CASCADE, to_field='sku')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, to_field='id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, to_field='id')
    product_status = models.ForeignKey('ProductStatus', on_delete=models.CASCADE, to_field='id')
    sku = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(default='No description')
    regular_price  = models.FloatField(blank=False, null=False, default=0.00)
    discount_price = models.FloatField(blank=True, default=0.00)
    quantity = models.IntegerField(default=1, null=False)
    taxable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
