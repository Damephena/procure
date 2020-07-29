from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response

import orders.serializers as serializers
from orders.models import OrderProduct, Order, Payment, Refund

from products.models import Product
from accounts.models import Address
from utils.paystack import Transaction, verify_payment

class OrderSummaryView(generics.ListAPIView):
    '''
    Order summary or Cart.
    '''
    serializer_class = serializers.OrderProductSerializer
    queryset = OrderProduct.objects.all()

    def get(self, request):
        try:
            order_product = OrderProduct.objects.get(user=self.request.user, ordered=False)
            order_product.refresh_from_db()
        except OrderProduct.DoesNotExist:
            return Response({'error': 'No Ordered Product'})
        serializer = self.serializer_class(order_product, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CheckoutView(generics.ListAPIView):
    '''
    CheckOut details including shipping address to continue with payment.
    '''
    serializer_class = serializers.CheckoutSerializer

    def get(self, request):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            order.refresh_from_db()
        except Order.DoesNotExist:
            return Response({"error": "You have no active order to checkout!"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(order, many=False)
        
        if not order.shipping_address:
            address_queryset = Address.objects.filter(user=self.request.user)

            if address_queryset.exists():
                order.shipping_address = address_queryset[0]
                order.save()

                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'Kindly provide a shipping address'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AddressCreateView(generics.ListCreateAPIView):
    '''
    Add Address to enable delivery.
    '''
    serializer_class = serializers.AddressSerializer

    def post(self, request):
        address = Address.objects.filter(user=self.request.user)
        if address.exists():
            return Response({"error": "You already have an address. Edit it"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressUpdateView(generics.RetrieveUpdateAPIView):
    '''
    Retrieve or Update Address details by User ID.
    '''
    serializer_class = serializers.AddressSerializer
    queryset = Address.objects.all()
    lookup_field = 'user'


class PaymentView(generics.CreateAPIView):
    '''
    Make payments.    
    @returns url: Authorization url to continue with Paystack's checkout screen.
    '''
    serializer_class = serializers.TransactionChargeSerializer

    def post(self, request):
        order_query = Order.objects.filter(user=self.request.user, ordered=False)

        if order_query.exists():
            order = order_query[0]
            total_price = order.get_total()

            # initialize payment
            trans = Transaction(
                self.request.user.email,
                total_price
            )
            initialize_transaction = trans.initialize_transaction()

            if initialize_transaction:
                order.ref_code = initialize_transaction['data']['reference']
                order.save()

                return Response({
                'data': initialize_transaction['data'],
                'message': initialize_transaction['message']
                }, 
                status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': initialize_transaction['message']
                },
                status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

class VerifyPaymentView(generics.CreateAPIView):
    '''
    Verify payment was made by customer.
    @params string: reference code of payment.
    '''
    serializer_class = serializers.VerifyPaymentSerializer

    def post(self, request):
        try:
            q = Order.objects.get(user=self.request.user, ref_code=self.request.data['reference'])
        except Order.DoesNotExist:
            return Response({"error": "No such reference code. Please check entry!"}, status=status.HTTP_404_NOT_FOUND)
        if q.ordered:
            q.order_items.update(ordered=True)
            return Response({"message": "Payment confirmed!"})
        
        order_query = Order.objects.filter(user=self.request.user, ref_code=self.request.data['reference'], ordered=False)

        if order_query.exists():
            order = order_query[0]

            verify = verify_payment(order.ref_code)

            if verify['data']['status'] == 'success':
                payment = Payment.objects.create(
                    user=self.request.user,
                    paystack_id=verify['data']['id'],
                    amount=verify['data']['amount']/100
                )
                order.ordered = True
                order.payment = payment
                order.save()

                order.order_items.update(ordered=True)

                return Response({'message': 'Payment confirmed successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response(verify_payment, status=status.HTTP_402_PAYMENT_REQUIRED)
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)



class OrderHistory(generics.ListAPIView):
    '''
    Returns all orders that has been paid for.
    '''
    serializer_class = serializers.OrderSerializer

    def get(self, request):
        orders = Order.objects.filter(user=self.request.user, ordered=True)
        serializer = self.serializer_class(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AddToCartView(generics.CreateAPIView):
    '''
    Add a product to existing or new cart. If cart with product already exists, 
    increments by 1.
    '''
    serializer_class = (serializers.OrderSerializer, serializers.OrderProductSerializer,)

    def post(self, request, slug):
        item = get_object_or_404(Product, slug=slug)
        order_item, created = OrderProduct.objects.get_or_create(
            product=item,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]
            cart_serializer = self.serializer_class[1](order_item)
            
            # check if the order item is in the order
            if order.order_items.filter(product__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                
                return Response(data={
                    'message': 'This item has been updated',
                    'cart': cart_serializer.data,
                    }, status=status.HTTP_200_OK)
            else:
                order.order_items.add(order_item)
                return Response(data={
                    'message': 'This product has been added to your cart',
                    'cart' : cart_serializer.data,
                    }, 
                    status=status.HTTP_201_CREATED
                    )
        else:
            order = Order.objects.create(
                user=request.user,
            )
            order.order_items.add(order_item)
            order_serializer = self.serializer_class[0](order)

            if order_serializer.is_valid(raise_exception=True):
                order_serializer.save()
                cart_serializer = self.serializer_class[1](order_item)
                return Response(data={
                    'message' : 'New cart has been created',
                    'cart': cart_serializer.data,
                    # 'order': order_serializer.data,
                    }
                    , status=status.HTTP_201_CREATED)

           
class RemoveFromCartView(generics.CreateAPIView):
    '''
    Removes a product from existing cart.
    '''
    serializer_class = (serializers.OrderSerializer, serializers.OrderProductSerializer,)

    def post(self, request, slug):
        
        item = get_object_or_404(Product, slug=slug)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            query = order.order_items.filter(product__slug=item.slug, ordered=False)
            # check if the order product is in the order
            if query:
                order_item = OrderProduct.objects.filter(
                    product=item,
                    user=request.user,
                )[0]
                order.order_items.remove(order_item)
                order_item.delete()

                cart_serializer = self.serializer_class[1](order_item)
                return Response(data={
                'message': 'This product has been removed to your cart',
                'cart': cart_serializer.data,
                },
                status=status.HTTP_200_OK
                )

            order_serializer = self.serializer_class[0](order)
            return Response(data={
                'error': 'This product is not in your cart',
                'cart': order_serializer.data.get('order_items')
            },
            status=status.HTTP_404_NOT_FOUND
            )
        order_serializer = self.serializer_class[0](order_qs)
        return Response(data={
            'error': 'You do not have an active order',
            'order': order_serializer.data
        }, status=status.HTTP_404_NOT_FOUND)


class RemoveSingleItemView(generics.CreateAPIView):
    '''
    Update quantity of a particular product in cart. Decrement by 1.
    '''
    serializer_class = (serializers.OrderSerializer, serializers.OrderProductSerializer)

    def post(self, request, slug):
        item = get_object_or_404(Product, slug=slug)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        
        if order_qs.exists():
            order = order_qs[0]
            query = order.order_items.filter(product__slug=item.slug)
            order_serializer = self.serializer_class[0](order)

            #check if the order product is in the order
            if query.exists():
                order_item = OrderProduct.objects.filter(
                    product = item,
                    user = request.user
                )[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order.order_items.remove(order_item)
                    order_item.delete()
                
                cart_serializer = self.serializer_class[1](order_item)
                return Response(data={
                    'message': 'This product quantity has been updated',
                    'cart': cart_serializer.data,
                },
                status=status.HTTP_200_OK
                )
            else:
                return Response(data={
                    'error': 'This product is not in your cart',
                    'cart': order_serializer.data.get('order_items')
                },
                status=status.HTTP_404_NOT_FOUND
                )
            
            # deletes order from Order model if order_items is empty
            if not order.order_items.all():
                order.delete()
                return Response(data={
                    'error': 'No active order',
                },
                status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(data={
            'error': 'No active order'},
            status=status.HTTP_404_NOT_FOUND
        )

class RequestRefundView(generics.CreateAPIView):
    '''
    Request a refund.
    '''
    serializer_class = serializers.RefundSerializer

    def post(self, request):
        try:
            order = Order.objects.get(id=self.request.data['order'], ordered=True)
        except Order.DoesNotExist:
            return Response({"error": "Order with given ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        refund = Refund.objects.filter(order=self.request.data['order'])
        if refund.exists():
            return Response({"error": "A refund request already exists."}, status=status.HTTP_208_ALREADY_REPORTED)

        serializer = self.serializer_class(data=self.request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            order.refund_requested = True
            order.save()

            return Response(data={
                "message": "Your refund request has been sent",
                "data": serializer.data
                }, 
                status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

