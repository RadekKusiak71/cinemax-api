from collections import defaultdict
from datetime import timedelta

from django.db.models import (DateTimeField, DurationField, Exists,
                              ExpressionWrapper, F, OuterRef, QuerySet)
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   OpenApiResponse, extend_schema)
from rest_framework import permissions, status
from rest_framework.generics import (ListAPIView, RetrieveAPIView,
                                     get_object_or_404)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from movies.models import Movie
from reservations.models import ReservationStatus, Ticket
from showings.models import Showing
from showings.serializers import (GroupedShowingSerializer,
                                  ShowingDetailsSerializer,
                                  ShowingRoomLayoutSerializer)
from theaters.models import Seat


@extend_schema(
    summary='Retrieve detailed information about a specific showing.',
    description='Endpoint to retrieve detailed information about a specific showing by its ID.',
    tags=['Showings'],
    responses={
        status.HTTP_200_OK: ShowingDetailsSerializer,
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='Showing not found.',
            examples=[
                OpenApiExample(
                    name='Showing Not Found',
                    value={'detail': 'Not found.'},
                    response_only=True,
                    status_codes=[status.HTTP_404_NOT_FOUND],
                )
            ],
        )
    }
)
class RetrieveShowingAPIView(RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShowingDetailsSerializer
    queryset = (
        Showing.objects.all()
        .select_related(
            'variant', 
            'variant__movie',
            'theater_hall',
        )
        .annotate(
            movie_duration=ExpressionWrapper(
                (F('variant__movie__duration') + Showing.CLEANUP_BUFFER_MINUTES) * timedelta(minutes=1),
                output_field=DurationField()
            )
        )
        .annotate(
            end_time=ExpressionWrapper(
                F("start_time") + F('movie_duration'),
                output_field=DateTimeField(),
            )
        )
    )


@extend_schema(
    summary='List all seats for a showing.',
    description='Lists all seats for a showing specified by `showing_id` with flag that determines if seat is reserved.',
    tags=['Showings'],
    responses={
        status.HTTP_200_OK: ShowingRoomLayoutSerializer(many=True),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            description='Showing not found.',
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    'Showing Not Found',
                    summary='Showing Not Found',
                    description='The specified showing does not exist.',
                    value={
                        'detail': 'Not found.'
                    },
                    status_codes=[status.HTTP_404_NOT_FOUND],
                )
            ]
        )
    }
)
class RetrieveShowingRoomLayoutAPIView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShowingRoomLayoutSerializer
    pagination_class = None

    def get_queryset(self, showing: Showing) -> QuerySet[Showing]:
        return Seat.objects.filter(
            theater_hall__showings=showing,
        ).annotate(
            is_reserved=Exists(
                Ticket.objects.filter(
                    reservation__status__in=[ReservationStatus.CONFIRMED, ReservationStatus.PENDING],
                    reservation__showing=showing,
                    seat_id=OuterRef('pk')
                )
            )
        ).order_by('row', 'number')

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset: QuerySet[Seat] = self.get_queryset(
            showing=get_object_or_404(Showing, pk=self.kwargs.get('showing_id'))
        )
        serializer: ShowingRoomLayoutSerializer = ShowingRoomLayoutSerializer(
            queryset, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    summary='List availalbe showings for a movie in specified theater.',
    description='Lists availalbe showings `start_times` with `variant_key` ' \
    'representing movie type (e.g 2D English Subtitles) for a movie in specified theater.',
    tags=['Showings'],
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
    pagination_class = None
    
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