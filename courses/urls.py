from django.urls import path
from .views import PaymentView, SubscriptionView   # оставляем только Stripe и подписку
from django.urls import path
from .views import payment_success, payment_cancel
urlpatterns = [
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path('pay/', PaymentView.as_view(), name='payment'),  # Stripe оплата
    path('payment/success', payment_success, name='payment_success'),
    path('payment/cancel', payment_cancel, name='payment_cancel'),
]
