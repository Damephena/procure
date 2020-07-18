from rest_framework import serializers

import products.models as mod


class ImageSerializer(serializers.ModelSerializer):
    '''Images serializer.'''
    class Meta:
        model = mod.ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    '''Product serializer.'''
    class Meta:
        model = mod.Product
        exclude = ['created_at', 'updated_at', 'sku']
        read_only_kwargs = ['id']
        depth = 1


class ProductStatusSerializer(serializers.ModelSerializer):
    '''
    Create statuses which would be attached to each `product`.
    '''
    class Meta:
        model = mod.ProductStatus
        fields = '__all__'
        read_only_kwargs = ['id']


class CategorySerializer(serializers.ModelSerializer):
    '''
    Standalone categories which can be attached to a `product` in `ProductCategory`.
    '''
    class Meta:
        model = mod.Category
        fields = '__all__'
        read_only_kwargs = ['id']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Standalone tags that could be added to `product`s via `ProductTag` model.
    '''
    class Meta:
        model = mod.Tag
        fields = '__all__'
        read_only_kwargs = ['id']


class CouponSerializer(serializers.ModelSerializer):
    '''
    Coupons for each `product`. Optional parameter.
    '''
    class Meta:
        model = mod.Coupon
        fields = '__all__'
        read_only_kwargs = ['id']
