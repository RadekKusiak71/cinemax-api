import stripe
from django.conf import settings
from payments.events import StripeWebhookService
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

class StripeWebhookView(GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        StripeWebhookService().process(
            stripe.Webhook.construct_event(
                payload=request.body,
                sig_header=request.META['HTTP_STRIPE_SIGNATURE'],
                secret=settings.STRIPE_WEBHOOK_SECRET
            )
        )
        return Response(status=status.HTTP_200_OK)