from rest_framework import serializers

from movies.serializers import MovieDetailSerializer
from showings.models import Showing
from theaters.models import Seat


class ShowingDetailsSerializer(serializers.ModelSerializer):
    end_time = serializers.DateTimeField(help_text='Calculated end time of the showing including cleanup buffer.')
    theater_hall = serializers.CharField(source='theater_hall.number', help_text='Name of the theater hall where the showing takes place.')
    movie = MovieDetailSerializer(source='variant.movie', help_text='Detailed information about the movie being shown.')
    variant = serializers.StringRelatedField(help_text='Variant of the movie (e.g., 2D Original Japan, 2D Subtitles English).')
    
    class Meta:
        model = Showing
        fields = [
            'id', 
            'start_time', 
            'end_time',
            'theater_hall', 
            'movie',
            'variant'
        ]

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