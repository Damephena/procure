from django.urls import path
import orders.views as view

urlpatterns = [
    path('checkout/', view.CheckoutView.as_view(), name='checkout'),
    path('order-summary/', view.OrderSummaryView.as_view(), name='order-summary'),
    path('address/', view.AddressCreateView.as_view(), name='address-list'),
    path('address/<user>/', view.AddressUpdateView.as_view(), name='address-detail'),
    path('add-to-cart/<slug>/', view.AddToCartView.as_view(), name='cart-add'),
    path('remove-from-cart/<slug>/', view.RemoveFromCartView.as_view(), name='cart-remove-product'),
    path('reduce-item-in-cart/<slug>/', view.RemoveSingleItemView.as_view(), name='cart-reduce-product'),
    path('payment/', view.PaymentView.as_view(), name='payment'),
    path('payment/verify/', view.VerifyPaymentView.as_view(), name='verify-payment'),
    path('history/', view.OrderHistory.as_view(), name='order-history'),
    path('request-refund/', view.RequestRefundView.as_view(), name='request-refund'),
]
