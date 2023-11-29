from django.conf import settings

from education.models import Course
import stripe

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_session(course_id):
    if course_id:
        course = Course.objects.get(pk=course_id)

        product = stripe.Product.create(name=course.title)

        price = stripe.Price.create(
            unit_amount=course.price*100,
            currency="usd",
            product=product.id,
        )

        session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[
                {
                    "price": price.id,
                    "quantity": 1,
                },
            ],
            mode="payment",
        )

    return session.id, session.url


def check_payment(payments):
    for payment in payments:
        session_id = payment.session_id
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                payment.is_paid = True
                payment.save()
        except stripe.error.InvalidRequestError as e:
            # Invalid session ID
            pass
