from django.contrib.auth import get_user_model

from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

from orders.models import OrderProduct, Order, Payment, Refund
from accounts.models import Address

class AddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'
        read_only_kwargs = ['id', 'is_completed']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class TransactionChargeSerializer(serializers.Serializer):
    '''
    Serializer to allow user provide bank_code and account number to authenticate payment
    '''
    bank_code = serializers.CharField(max_length=10, help_text="Bank code from list of banks API endpoint")
    bank_account = serializers.CharField(max_length=15, help_text="Enter bank account for transaction")


class VerifyPaymentSerializer(serializers.Serializer):
    '''
    order ref code to be verified.
    '''
    reference = serializers.CharField(max_length=50)


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'
        read_only_fields = ['accepted']


class CheckoutSerializer(serializers.ModelSerializer):
    order_items = OrderProductSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    items_quantity = serializers.SerializerMethodField()
    shipping_address = AddressSerializer(many=False, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def get_total(self, obj):
        return obj.get_total()

    def get_items_quantity(self, obj):
        return obj.get_items_quantity()


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderProductSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
