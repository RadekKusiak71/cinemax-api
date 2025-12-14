from collections import defaultdict

from django.db.models import QuerySet
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   OpenApiResponse, extend_schema)
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from movies.models import Movie
from showings.models import Showing
from showings.serializers import GroupedShowingSerializer


@extend_schema(
    summary='List availalbe showings for a movie in specified theater.',
    description='Lists availalbe showings `start_times` with `variant_key` ' \
    'representing movie type (e.g 2D English Subtitles) for a movie in specified theater.',
    tags=['Screenings'],
    parameters=[
        OpenApiParameter(
            name='date',
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            description='Date to filter showings. Format: YYYY-MM-DD. Defaults to today if not provided.',
            required=False,
        )
    ],
    responses={
        status.HTTP_200_OK: GroupedShowingSerializer(many=True),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            description='Movie not found.',
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    'Movie Not Found',
                    summary='Movie Not Found',
                    description='The specified movie does not exist.',
                    value={
                        'detail': 'Not found.'
                    },
                    status_codes=[status.HTTP_404_NOT_FOUND],
                )
            ]
        )
    }
)
class ListMovieShowingsAPIView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = GroupedShowingSerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self, movie: Movie) -> QuerySet[Showing]:
        return Showing.objects.filter(
            variant__movie_id=self.kwargs.get('movie_id'),
            start_time__date=self.request.query_params.get(
                'date', timezone.now().date()
            ),
        ).select_related('variant')

    def group_showings_by_variant(self, showings: QuerySet[Showing]) -> list[dict[str, str | list]]:
        grouped_showings = defaultdict(list)

        for showing in showings:
            grouped_showings[str(showing.variant)].append(
                showing
            )

        return [
            {
                'variant_key': variant,
                'showings': showings
            } for variant, showings in grouped_showings.items()
        ]
    
    def list(self, request: Request, *args, **kwargs) -> Response:
        grouped_data: list[dict[str, str | list]] = self.group_showings_by_variant(self.get_queryset(
            movie=get_object_or_404(Movie, pk=self.kwargs.get('movie_id'))
        ))
        serializer: GroupedShowingSerializer = self.get_serializer(grouped_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)