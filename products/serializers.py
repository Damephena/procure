from rest_framework import serializers

import products.models as mod


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = mod.Product
        fields = '__all__'
        read_only_kwargs = ['id']
