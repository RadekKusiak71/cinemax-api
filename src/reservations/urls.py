from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reservations.views import ReservationViewSet

app_name = 'reservations'

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename='reservations')

urlpatterns = [
    path('', include(router.urls)),
]
