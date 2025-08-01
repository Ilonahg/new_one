import stripe
from django.conf import settings

# Используем ключ из settings.py
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(course):
    """
    Создаёт Stripe-продукт, цену и checkout-сессию.
    """
    # Создаём продукт в Stripe
    product = stripe.Product.create(name=course.title)

    # Создаём цену в Stripe (в центах)
    price = stripe.Price.create(
        unit_amount=int(course.price * 100),
        currency="usd",
        product=product.id,
    )

    # ✅ Создаём checkout-сессию с правильными URL
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": price.id,
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://127.0.0.1:8000/payment/success",  # 👈 поменяли
        cancel_url="http://127.0.0.1:8000/payment/cancel",    # 👈 поменяли
    )

    return session
