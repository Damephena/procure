from django.contrib import admin
import products.models as model

admin.site.register(model.Category)
admin.site.register(model.Coupon)
admin.site.register(model.Product)
admin.site.register(model.ProductImage)
admin.site.register(model.ProductStatus)
admin.site.register(model.Tag)
