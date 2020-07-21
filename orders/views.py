from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

import orders.serializers as serializers
from orders.models import OrderProduct, Order

from products.models import Product
from utils.permissions import IsOwner, AnonCreateAndUpdateOwnerOnly


class OrderSummaryView(generics.ListAPIView):
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()

    def get(self, request):
        queryset = Order.objects.get(user=self.request.user, ordered=False)
        seralizer = self.serializer_class(queryset, many=False)
        return Response(data=seralizer.data, status=status.HTTP_200_OK)

class CheckoutView(generics.ListCreateAPIView):
    serializer_class = serializers.CheckoutSerializer

    def get(self, request):
        queryset = Order.objects.filter(user=self.request.user, ordered=False)
        serializer = self.serializer_class(queryset, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# class PaymentViewSet(viewsets.ModelViewSet):
class PaymentViewSet(generics.ListCreateAPIView):
    serializer_class = serializers.PaymentSerializer

    def order_queryset(self):
        return Order.objects.get(user=self.request.user, ordered=False)
    
    # def list(self, request):
    def get(self, request):
        order = self.order_queryset()

        context = {
            'order': order,
            # 'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY
        }
        if order.shipping_address:
            userprofile = self.request.user.userprofile
            if userprofile.one_clicking_purchasing:
                # fetch the user's card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    context.update({
                        'card': card_list[0]
                    })
            return Response(data=context, status=status.HTTP_200_OK)
        return Response(data={'error': 'No shipping address'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # def create(self, request):
    def post(self, request):
        order = self.order_queryset()
        serializer = serializers.PaymentSerializer(order)
        userprofile = UserProfile.objects.get(user=self.request.user)

        if serializer.is_valid(raise_exception=True):
            token = self.request.data['stripeToken']
            save = self.request.data['save']
            use_default = self.request.data['use_default']

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(userprofile.stripe_customer_id)
                    customer.sources.create(source=token)
                else:
                    customer = stripe.Customer.create(email=self.request.user.email)
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()
            amount = int(order.get_total() * 100)

            try:
                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount, # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,
                        currency='usd',
                        source=token
                    )
                
                # create the payment
                payment = Payment.objects.create(
                    stripe_charge_id = charge['id'],
                    user=self.request.user,
                    amount= order.get.total()
                )

                # assign payment to the order
                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()
                
                order.ordered = True
                order.payment = payment
                order.save()
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except:
                error = {}

                for err in stripe.error:
                    error[err] = err.message
                return Response(data=error, status=status.HTTP_400_BAD_REQUEST)

class AddToCartView(generics.CreateAPIView):
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
            # serializer = self.serializer_class[1](order_item)
            cart_serializer = self.serializer_class[1](order_item)
            # check if the order item is in the order
            if order.order_items.filter(product__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                
                return Response(data={
                    'message': 'This item has been updated',
                    # 'cart': serializer.data.get('order_items')
                    'cart': cart_serializer.data,
                    }, status=status.HTTP_200_OK)
            else:
                order.order_items.add(order_item)
                # serializer = self.serializer_classes[0](order)
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
                # cart_serializer = self.serializer_class[1](order_item)
                return Response(data={
                    'message' : 'New cart has been created',
                    # 'cart': cart_serializer.data,
                    'order': order_serializer.data,
                    }
                    , status=status.HTTP_201_CREATED)

           
class RemoveFromCartView(generics.CreateAPIView):
    serializer_classes = (serializers.OrderSerializer, serializers.OrderProductSerializer,)

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
                order_serializer = self.serializer_classes[0](order)
                cart_serializer = self.serializer_classes[1](order_item)
                return Response(data={
                'message': 'This product has been removed to your cart',
                'cart': cart_serializer.data,
                'order': order_serializer.data
                },
                status=status.HTTP_200_OK
                )
            else:
                order_serializer = self.serializer_classes[0](order)
                return Response(data={
                    'error': 'This product is not in your cart',
                    'order': order_serializer.data
                },
                status=status.HTTP_404_NOT_FOUND
                )
        order_serializer = self.serializer_classes[0](order_qs)
        return Response(data={
            'error': 'You do not have an active order',
            'order': order_serializer.errors
        })


class RemoveSingleItemView(generics.CreateAPIView):
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
                    'order': order_serializer.data
                },
                status=status.HTTP_200_OK
                )
            else:
                return Response(data={
                    'error': 'This product is not in your cart',
                    'order': order_serializer.data
                },
                status=status.HTTP_404_NOT_FOUND
                )
            
            # deletes order from Order model if order_items is empty
            if not order.order_items.all():
                order.delete()
                return Response({'error': 'No active order'})
        
        return Response(data={
            'error': 'You do not have an active order',
        })


# def add_to_cart(request, slug):
#     item = get_object_or_404(Product, slug=slug)
#     order_product, created = OrderProduct.objects.get_or_create(
#         product=item,
#         user=request.user,
#         ordered=False
#     )
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.order_items.filter(product__slug=item.slug).exists():
#             order_item.quantity += 1
#             order_item.save()

#             return Response(data={'message': 'This item has been updated'}, status=status.HTTP_200_OK)
#         else:
#             order.order_items.add(order_item)
#             return Response(data={
#                 'message': 'This product has been added to your cart',
#                 'cart' : order,
#                 }, 
#                 status=status.HTTP_201_CREATED
#                 )
#     else:
#         order = Order.objects.create(
#             user=request.user,
#         )
#         order.order_items.add(order_item)
#         return Response(data={
#             'message': 'This product has been added to your cart',
#             'cart': order
#             },
#             status=status.HTTP_201_CREATED
#         )

# @login_required
# def remove_from_cart(request, slug):
#     item = get_object_or_404(Product, slug=slug)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]

#         # check if the order product is in the order
#         if order.order_items.filter(product__slug=item.slug):
#             order_item = OrderProduct.objects.filter(
#                 product=item,
#                 user=request.user,
#             )[0]
#             order.order_items.remove(order_item)
#             order_item.delete()

#             return Response(data={
#             'message': 'This product has been removed to your cart',
#             'cart': order
#             },
#             status=status.HTTP_201_CREATED
#             )
#         else:
#             return Response(data={
#                 'error': 'This product is not in your cart',
#                 'cart': order
#             },
#             status=status.HTTP_404_NOT_FOUND
#             )
#     return Response(data={
#         'error': 'You do not have an active order' 
#     })

# @login_required
# def remove_single_item_from_cart(request, slug):
#     item = get_object_or_404(Product, slug=slug)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]

#         #check if the order product is in the order
#         if order.order_items.filter(product__slug=item.slug).exists():
#             order_item = OrderProduct.objects.filter(
#                 order_item = item,
#                 user = request.user
#             )[0]
#             if order_item.quantity > 1:
#                 order_item.quantity -= 1
#                 order_item.save()
#             else:
#                 order.order_items.remove(order_item)
#             return Response(data={
#                 'message': 'This product quantity has been updated',
#                 'cart': order
#             },
#             status=status.HTTP_200_OK
#             )
#         else:
#             return Response(data={
#                 'error': 'This product is not in your cart',
#                 'cart': order
#             },
#             status=status.HTTP_404_NOT_FOUND
#             )
#     return Response(data={
#         'error': 'You do not have an active order',
#     })


# def update_product_unit(product_id, unit):
#     product = Product.objects.select_for_update().filter(id=product_id)

#     with transaction.atomic():
#         if product.quantity - unit < 0:
#             raise ValueError('You are trying to order more than what is currently available')
#         product.quantity = product.quantity - unit
#         return product

# def add_to_cart(self, request):
#     items = Order.objects.select_for_update().filter(author=request.user)
#     cart = Order.objects.create(
#                 user=self.request.user, 
#                 order_items=self.request.data['product'],
#                 )
# class OrderProductViewset(viewsets.ModelViewSet):
#     queryset = OrderProduct.objects.all()
#     serializer_class = serializers.OrderProductSerializer
#     permission_classes = (IsOwner,)

#     def get_queryset(self):
#         user = self.request.user
#         return OrderProduct.objects.filter(user=user)

#     def list(self, request):
#         serializer = self.serializer_class(self.get_queryset(), many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)

#     def create(self, request):
#         data = self.request.data
#         # data['user'] = request.user.id
#         serializer = self.serializer_class(data=data, context={'request': request})

#         if serializer.is_valid(raise_exception=True):

#             # product = Product.objects.get(id=request.data['product'])
#             update_product_unit(self.request.data['product'].id, self.request.data['unit'])
#             serializer.save()
#             cart = ''
#             Product.refresh_from_db()
#             Order.refresh_from_db()
#             if cart:
#                 return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

