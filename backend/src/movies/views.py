from django.db.models import Min
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema)
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination

from movies.models import Movie
from movies.serializers import MovieDetailSerializer, MovieListSerializer


@extend_schema(
    tags=["Movies"],
    summary="Retrieve a list of currently playing movies in theater",
    description="Endpoint to retrieve a list of all movies that are currently playing or have scheduled screenings in theater.",
    responses={
        status.HTTP_200_OK: MovieListSerializer(many=True),
    }
)
class MovieListAPIView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MovieListSerializer
    pagination_class = LimitOffsetPagination
    queryset = (
        Movie.objects
        .filter(showing_variants__showings__start_time__gt=timezone.now())
        .annotate(earliest_showing_time=Min('showing_variants__showings__start_time'))
        .order_by('earliest_showing_time', 'title')
    )

@extend_schema(
    tags=["Movies"],
    summary="Retrieve detailed information about a specific movie",
    description="Endpoint to retrieve detailed information about a specific movie by its ID.",
    responses={
        status.HTTP_200_OK: MovieDetailSerializer,
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Movie not found.",
            examples=[
                OpenApiExample(
                    name="Movie Not Found",
                    value={"detail": "Not found."},
                    response_only=True,
                    status_codes=[status.HTTP_404_NOT_FOUND],
                )
            ],
        )
    }
)
class MovieDetailAPIView(RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MovieDetailSerializer
    queryset =(
        Movie.objects.all()
        .select_related('original_language', 'director')
        .prefetch_related('genres')
    )