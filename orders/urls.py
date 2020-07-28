from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
import orders.views as view
router = SimpleRouter()

urlpatterns = [
    path('checkout/', view.CheckoutView.as_view(), name='checkout'),
    path('order-summary/', view.OrderSummaryView.as_view(), name='order-summary'),
    path('address/', view.AddressCreateView.as_view(), name='address-list'),
    path('address/<user>/', view.AddressUpdateView.as_view(), name='address-detail'),
    path('add-to-cart/<slug>/', view.AddToCartView.as_view(), name='cart-add'),
    path('remove-from-cart/<slug>/', view.RemoveFromCartView.as_view(), name='cart-remove'),
    path('remove-item-from-cart/<slug>/', view.RemoveSingleItemView.as_view(), name='cart-remove-single-item'),
    path('payment/', view.PaymentView.as_view(), name='payment'),
    path('payment/verify/', view.VerifyPaymentView.as_view(), name='verify-payment'),
]

urlpatterns += router.urls
