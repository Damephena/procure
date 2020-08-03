from PIL import Image

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters import rest_framework as filters

from rest_framework import generics, status, viewsets, views
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny

import products.serializers as serializers 
from products.models import (
    Category,
    Coupon,
    Product,
    ProductImage,
    ProductStatus,
    Tag,
)


class ImageUploadParser(FileUploadParser):
    '''Inherits `FileUploadParser` to specify image media types only.'''
    media_type = 'image/*'


class ProductFilter(filters.FilterSet):
    '''Custom filterset for filtering `product` view'''
    min_price = filters.NumberFilter(field_name="regular_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="regular_price", lookup_expr='lte')
    class Meta:
        model = Product
        fields = ('name', 'category', 'tags', 'min_price', 'max_price', 'product_status__id')


class ImageUploadView(views.APIView):
    '''API endpoint for `Product` image upload and delete'''
    parser_class = (ImageUploadParser,)

    def post(self, request):
        photo = request.data['photo']

        try:
            img = Image.open(request.data['photo'])
            img.verify()
        except:
            raise ParserError(detail={'Unsupported file type!'}, code=status.HTTP_412_PRECONDITION_FAILED)
        serializer = serializers.ImageSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            ProductImage.image.delete(save=True)
        except:
            raise ParseError(detail={'Something went wrong'}, code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(data={'Image deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class ProductReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    '''List and retrieve all products.'''
    lookup_field = 'slug'
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    filterset_class = ProductFilter
    search_fields = ('name', 'category__name', 'tags__name')
    ordering_fields = ('name', 'category__name', 'tags__name')

class TagView(generics.ListAPIView):
    '''Gets all tags.'''
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    filterset_fields = ('name',)
    permission_classes = (AllowAny,)

class TagDetail(generics.RetrieveAPIView):
    '''Shows a tag's detail.'''
    look_up = 'pk'
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (AllowAny,)


class CategoryView(generics.ListAPIView):
    '''Gets all categories.'''
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (AllowAny,)


class CategoryDetail(generics.RetrieveAPIView):
    '''Shows a category's detail.'''
    look_up = 'pk'
    queryset = Category.objects.all()
    filterset_fields = ('name',)
    serializer_class = serializers.CategorySerializer
    permission_classes = (AllowAny,)


class ProductStatusView(generics.ListAPIView):
    '''Gets all categories.'''
    queryset = ProductStatus.objects.all()
    serializer_class = serializers.ProductStatusSerializer
    permission_classes = (AllowAny,)


# class CouponViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = serializers.CouponSerializer
#     queryset = Coupon.objects.all()
