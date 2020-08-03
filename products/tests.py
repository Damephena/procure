from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from products.models import Product, ProductStatus, Category, Tag


class ProductTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.client.post('/api/v1/rest-auth/registration/', data={
            'first_name': 'test',
            'last_name': 'user',
            'password1': 'passworddd1234',
            'password2': 'passworddd1234',
            'email': 'test@example.com',
        })

        self.response = self.client.post(reverse('rest_login'), data={
            'email': 'test@example.com',
            'password': 'passworddd1234',
        })
        self.token = self.response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)

        self.ps1 = ProductStatus.objects.create(name='in stock')
        self.t1 = Tag.objects.create(name='cheap')
        self.t2 = Tag.objects.create(name='cotton')
        self.t3 = Tag.objects.create(name='long-sleeve')
        self.c1 = Category.objects.create(name='T-shirt')

        self.product1 = Product.objects.create(
            category=self.c1,
            product_status=self.ps1,
            sku='p-1-c',
            name='Asia polo',
            regular_price=3750,
        )
        self.product1.tags.add(self.t1, self.t2)

        self.product2 = Product.objects.create(
            category=self.c1,
            product_status=self.ps1,
            sku='p-2-l',
            name='Nigerian polo',
            regular_price=6000,
        )
        self.product2.tags.add(self.t3, self.t2)

    def test_authenticated_user_can_get_all_products(self):
        response = self.client.get(reverse('products-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_get_product_detail(self):
        url = '/api/v1/products/' + str(self.product1.id) + '/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_get_all_tags(self):
        response = self.client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_get_tag_detail(self):
        url = '/api/v1/products/tags/' + str(self.t1.id) + '/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_get_all_categories(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_get_category_detail(self):
        url = '/api/v1/products/categories/' + str(self.t1.id) + '/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
