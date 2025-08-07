from django.urls import path
from .views import PaymentView, SubscriptionView   # ✅ оставляем только Stripe и подписку

urlpatterns = [
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path('pay/', PaymentView.as_view(), name='payment'),  # Stripe оплата
]
