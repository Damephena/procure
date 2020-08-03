from django.contrib import admin
import products.models as model

admin.site.register((
    model.Category, 
    model.Coupon, 
    model.Product, 
    model.ProductImage, 
    model.ProductStatus,
    model.Tag
))
