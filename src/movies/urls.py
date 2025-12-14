from django.urls import path
from movies.views import MovieListAPIView, MovieDetailAPIView

app_name = 'movies'

urlpatterns = [
    path('movies/', MovieListAPIView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),
]