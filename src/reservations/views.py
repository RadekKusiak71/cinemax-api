
from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema, extend_schema_view)
from rest_framework import mixins, permissions, serializers, status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from reservations.models import Reservation
from reservations.serializers import (CreateReservationSerializer,
                                      ReservationSerializer)
from reservations.services import cancel_reservation, create_reservation
from showings.models import Showing


@extend_schema_view(
    create=extend_schema(
        summary="Create reservation (booking) for a showing.",
        description=(
            "Creates a reservation for the authenticated user for a given showing and selected seats. "
            "If any seat is already reserved (PENDING/CONFIRMED) the request fails."
        ),
        tags=["Reservations"],
        request=CreateReservationSerializer,
        responses={
            status.HTTP_201_CREATED: ReservationSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Business rule validation error (e.g. seats already booked, too many seats, existing pending).",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Seats already booked",
                        value={"detail": "One or more of the selected seats are already booked."},
                        status_codes=[status.HTTP_400_BAD_REQUEST],
                    ),
                    OpenApiExample(
                        "Existing pending reservation",
                        value={"detail": "User already has a pending reservation for this showing."},
                        status_codes=[status.HTTP_400_BAD_REQUEST],
                    ),
                    OpenApiExample(
                        "Max seats exceeded",
                        value={"detail": "The maximum number of seats per reservation has been exceeded."},
                        status_codes=[status.HTTP_400_BAD_REQUEST],
                    ),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Showing not found (invalid showing_id).",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Showing not found",
                        value={"detail": "Not found."},
                        status_codes=[status.HTTP_404_NOT_FOUND],
                    )
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated.",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Unauthorized",
                        value={"detail": "Authentication credentials were not provided."},
                        status_codes=[status.HTTP_401_UNAUTHORIZED],
                    )
                ],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User is authenticated but not allowed (depends on auth configuration).",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Forbidden",
                        value={"detail": "You do not have permission to perform this action."},
                        status_codes=[status.HTTP_403_FORBIDDEN],
                    )
                ],
            ),
        },
        examples=[
            OpenApiExample(
                "Create reservation request",
                value={"showing_id": 123, "seat_ids": [10, 11, 12]},
                request_only=True,
            )
        ],
    ),
    destroy=extend_schema(
        summary="Cancel reservation (booking).",
        description=(
            "Cancels a reservation owned by the authenticated user. "
            "Only PENDING reservations can be canceled."
        ),
        tags=["Reservations"],
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="Reservation canceled."),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid reservation status (only PENDING can be canceled).",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Invalid status",
                        value={"detail": "Only pending reservations can be canceled."},
                        status_codes=[status.HTTP_400_BAD_REQUEST],
                    )
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Reservation not found (or not owned by user).",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Not found",
                        value={"detail": "Not found."},
                        status_codes=[status.HTTP_404_NOT_FOUND],
                    )
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated.",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Unauthorized",
                        value={"detail": "Authentication credentials were not provided."},
                        status_codes=[status.HTTP_401_UNAUTHORIZED],
                    )
                ],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User is authenticated but not allowed (depends on auth configuration).",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Forbidden",
                        value={"detail": "You do not have permission to perform this action."},
                        status_codes=[status.HTTP_403_FORBIDDEN],
                    )
                ],
            ),
        },
    ),
)
class ReservationViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "booking_id"

    def get_queryset(self) -> QuerySet[Reservation]:
        return Reservation.objects.filter(user=self.request.user)
    
    def get_serializer_class(self) -> type[serializers.Serializer]:
        if self.action == "create":
            return CreateReservationSerializer
        return super().get_serializer_class()

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_reservation: Reservation = create_reservation(
            seat_ids=serializer.validated_data.get("seat_ids"),
            showing=get_object_or_404(Showing, pk=serializer.validated_data.get("showing_id")), 
            user=request.user
        )

        return Response(ReservationSerializer(created_reservation).data, status=status.HTTP_201_CREATED)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        cancel_reservation(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)