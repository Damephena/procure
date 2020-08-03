import uuid
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=400, unique=True)
    description = models.TextField(max_length=250)
    active = models.BooleanField(default=False, blank=True)
    value = models.IntegerField(default=10, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    multiple = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class ProductStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)


    class Meta:
        ordering = ['name']
        verbose_name_plural = 'product statuses'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/product/', default='images/product/no-image.jpg', blank=True)
    description = models.TextField(default='No description', blank=True)

    def __str__(self):
        return self.image.name

# An SKU number is a unique code that is assigned to each product in a company's inventory. 
#  SKU stands for "Stock Keeping Unit"
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, to_field='id')
    product_status = models.ForeignKey('ProductStatus', on_delete=models.CASCADE, to_field='name')
    tags = models.ManyToManyField(Tag)
    product_image = models.ManyToManyField(ProductImage)
    slug = models.SlugField(blank=True, unique=True)
    sku = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(default='No description', blank=True)
    regular_price  = models.FloatField(blank=False, null=False, default=0.00)
    discount_price = models.FloatField(blank=True, default=0.00)
    quantity = models.IntegerField(default=1, null=False, blank=True)
    taxable = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + ': ' + self.category.name