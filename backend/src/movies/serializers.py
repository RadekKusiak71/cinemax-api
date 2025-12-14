from rest_framework import serializers

from movies.models import Director, Genre, Movie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'first_name', 'last_name']

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'poster_image', 'release_year']

class MovieDetailSerializer(serializers.ModelSerializer):
    original_language = serializers.CharField(source='original_language.name')
    genres = GenreSerializer(many=True)
    director = DirectorSerializer()

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'summary',
            'release_year',
            'poster_image',
            'duration',
            'age_restriction',
            'original_language',
            'genres',
            'director',
        ]