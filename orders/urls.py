from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
import orders.views as view
router = SimpleRouter()
# router.register('order-product', view.OrderProductViewset, basename='orders')
# router.register('checkout', view.CheckoutViewSet, basename='checkout')
# router.register('payment', view.CheckoutViewSet, basename='payment')

urlpatterns = [
    path('checkout/', view.CheckoutView.as_view(), name='checkout'),
    path('order-summary/', view.OrderSummaryView.as_view(), name='order-summary'),
    # path('add-to-cart/<slug>/', view.add_to_cart, name='add-to-cart'),
    # path('remove-from-cart/<slug>/', view.remove_from_cart, name='remove-from-cart'),
    # path('remove-item-from-cart/<slug>/', view.remove_single_item_from_cart,
    #      name='remove-single-item-from-cart'),
    path('add-to-cart/<slug>/', view.AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<slug>/', view.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', view.RemoveSingleItemView.as_view(), name='remove-single-item-from-cart'),
    # path('payment/<payment_option>/', view.PaymentView.as_view(), name='payment'),
]

urlpatterns += router.urls
