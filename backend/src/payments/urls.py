from django.urls import path
from payments.views import CreateCheckoutSessionAPIView, StripeWebhookView

app_name = "payments"

urlpatterns = [
    path(
        "reservations/<int:booking_id>/checkout/",
        CreateCheckoutSessionAPIView.as_view(),
        name="reservation-checkout",
    ),
    path(
        "webhook/stripe/",
        StripeWebhookView.as_view(),
        name="stripe-webhook",
    ),
]