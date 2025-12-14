import stripe
from django.conf import settings
from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema)
from rest_framework import permissions, serializers, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from payments.events import StripeWebhookService
from payments.exceptions import InvalidBookingStatusError
from payments.serializers import CheckoutSessionSerializer
from payments.services import create_checkout
from reservations.models import Reservation


@extend_schema(
    summary="Create Stripe Checkout session for reservation.",
    description=(
        "Creates a Stripe Checkout session for the authenticated user's reservation. "
        "Reservation must have status PENDING."
    ),
    tags=["Payments"],
    responses={
        status.HTTP_201_CREATED: CheckoutSessionSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Reservation is not in PENDING status (or other business rule error).",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    "Invalid booking status",
                    value={"detail": "Cannot checkout reservation 123: Status is CONFIRMED"},
                    status_codes=[status.HTTP_400_BAD_REQUEST],
                )
            ],
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description="Authentication required.",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    "Unauthorized",
                    value={"detail": "Authentication credentials were not provided."},
                    status_codes=[status.HTTP_401_UNAUTHORIZED],
                )
            ],
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            description="Reservation not found (or does not belong to user).",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    "Not found",
                    value={"detail": "Not found."},
                    status_codes=[status.HTTP_404_NOT_FOUND],
                )
            ],
        ),
    },
)
class CreateCheckoutSessionAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CheckoutSessionSerializer

    def get_queryset(self) -> QuerySet[Reservation]:
        return Reservation.objects.filter(user=self.request.user)

    def post(self, request: Request, booking_id: int, *args, **kwargs) -> Response:
        reservation: Reservation = get_object_or_404(self.get_queryset(), pk=booking_id)

        try:
            session = create_checkout(reservation)
        except InvalidBookingStatusError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        data = {"session_id": session.id, "url": session.url}
        return Response(self.get_serializer(data).data, status=status.HTTP_201_CREATED)

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