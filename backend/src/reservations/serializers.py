from rest_framework import serializers

from reservations.models import Reservation, Ticket


class ConfirmedReservationListSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(source="showing.variant.movie.id", read_only=True)
    movie_title = serializers.CharField(source="showing.variant.movie.title", read_only=True)
    movie_duration = serializers.IntegerField(source="showing.variant.movie.duration", read_only=True)
    movie_poster = serializers.ImageField(source="showing.variant.movie.poster_image", read_only=True)

    showing_id = serializers.IntegerField(source="showing.id", read_only=True)
    showing_start_time = serializers.DateTimeField(source="showing.start_time", read_only=True)
    theater_hall = serializers.CharField(source="showing.theater_hall.number", read_only=True)
    variant = serializers.StringRelatedField(source="showing.variant", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "created_at",
            "full_price",
            "status",
            "showing_id",
            "showing_start_time",
            "theater_hall",
            "variant",
            "movie_id",
            "movie_title",
            "movie_duration",
            "movie_poster",
        ]

class TicketInReservationSerializer(serializers.ModelSerializer):
    seat_row = serializers.IntegerField(source="seat.row", read_only=True)
    seat_number = serializers.IntegerField(source="seat.number", read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "price", "seat_row", "seat_number"]

class ConfirmedReservationDetailSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(source="showing.variant.movie.id", read_only=True)
    movie_title = serializers.CharField(source="showing.variant.movie.title", read_only=True)
    movie_duration = serializers.IntegerField(source="showing.variant.movie.duration", read_only=True)
    movie_poster = serializers.ImageField(source="showing.variant.movie.poster_image", read_only=True)
    showing_id = serializers.IntegerField(source="showing.id", read_only=True)
    showing_start_time = serializers.DateTimeField(source="showing.start_time", read_only=True)
    theater_hall = serializers.CharField(source="showing.theater_hall.number", read_only=True)
    variant = serializers.StringRelatedField(source="showing.variant", read_only=True)
    tickets = TicketInReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "created_at",
            "full_price",
            "status",
            "showing_id",
            "showing_start_time",
            "theater_hall",
            "variant",
            "movie_id",
            "movie_title",
            "movie_duration",
            "movie_poster",
            "tickets",
        ]

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