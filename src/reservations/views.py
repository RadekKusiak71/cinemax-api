
from django.db.models import QuerySet
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