from rest_framework import serializers

from reservations.models import Reservation


class CreateReservationSerializer(serializers.Serializer):
    seat_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        allow_empty=False,
        help_text="List of seat IDs to reserve"
    )
    showing_id = serializers.IntegerField(
        help_text="ID of the showing for which the reservation is being made"
    )



class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'id',
            'full_price',
            'status',
            'created_at',
            'updated_at',
        ]