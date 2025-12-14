from rest_framework import serializers

from showings.models import Showing
from theaters.models import Seat


class ShowingRoomLayoutSerializer(serializers.ModelSerializer):
    is_reserved = serializers.BooleanField(help_text='Indicates if the seat is reserved for the showing.')
    
    class Meta:
        model = Seat
        fields = ['id', 'row', 'number', 'is_reserved']


class ShowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showing
        fields = ['id', 'start_time']

class GroupedShowingSerializer(serializers.Serializer):
    variant_key = serializers.CharField(help_text='Key that represents movie format (e.g 2D Original Japan, 2D Subtitles English)')
    showings = ShowingSerializer(many=True)