from django.urls import path

from movies.views import MovieDetailAPIView, MovieListAPIView
from showings.views import ListMovieShowingsAPIView

app_name = 'movies'

urlpatterns = [
    path('movies/', MovieListAPIView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),
    path('movies/<int:movie_id>/showings/', ListMovieShowingsAPIView.as_view(), name='list-movie-showings'),
]