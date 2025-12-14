from rest_framework import serializers

from showings.models import Showing


class ShowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showing
        fields = ['id', 'start_time']

class GroupedShowingSerializer(serializers.Serializer):
    variant_key = serializers.CharField(help_text='Key that represents movie format (e.g 2D Original Japan, 2D Subtitles English)')
    showings = ShowingSerializer(many=True)