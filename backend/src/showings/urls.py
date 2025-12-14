from django.urls import path

from showings.views import RetrieveShowingRoomLayoutAPIView, RetrieveShowingAPIView

app_name = 'showings'

urlpatterns = [
    path('showings/<int:showing_id>/room-layout/', RetrieveShowingRoomLayoutAPIView.as_view(), name='showing-room-layout'),
    path('showings/<int:pk>/', RetrieveShowingAPIView.as_view(), name='showing-detail'),
]
