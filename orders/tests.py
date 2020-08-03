from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from orders.models import OrderProduct, Order, Payment, Refund
from products.models import Product, ProductStatus, Tag, Category

class OrderTestCase(APITestCase):
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
        self.user2 = get_user_model().objects.create_user(
            email='test2@example.com',
            password='passworddd1234',
            first_name='test2',
            last_name='user2'
        )

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
    
    def test_user_can_add_shipping_address(self):
        url = '/api/v1/orders/address/'
        data = {
            'address_line_1': 'a place',
            'town_city': 'Ikeja',
            'state': 'Lagos',
            'country': 'NG',
            'phone_number': '+2347032145678'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_can_retrieve_shipping_address(self):
        url = '/api/v1/orders/address/' + self.user.data['user']['pk'] + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_shipping_address(self):
        user_id = self.user.data['user']['pk']

        url = '/api/v1/orders/address/' + user_id + '/'
        data = {
            'address_line_1': 'Shoprite road',
            'town_city': 'Ikeja',
            'state': 'Lagos',
            'country': 'NG',
            'phone_number': '+2347032145679'
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_add_to_cart(self):
        url = '/api/v1/orders/add-to-cart/' + self.product1.slug + '/'
        response = self.client.post(url, data={'slug': self.product1.slug})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_can_reduce_item_quantity(self):
        url = 'api/v1/orders/reduce-item-in-cart/' + self.product1.slug + '/'
        response = self.client.post(url, data={'slug': self.product1.slug})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
