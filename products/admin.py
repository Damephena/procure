from django.contrib import admin
import products.models as model

# Register your models here.
admin.site.register(model.Category)
admin.site.register(model.Coupon)
admin.site.register(model.Product)
admin.site.register(model.ProductCategory)
admin.site.register(model.ProductStatus)
admin.site.register(model.ProductTag)
admin.site.register(model.Tag)
