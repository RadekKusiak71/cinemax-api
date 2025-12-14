from django.urls import path

from showings.views import RetrieveShowingRoomLayoutAPIView

app_name = 'showings'

urlpatterns = [
    path('showings/<int:showing_id>/room-layout/', RetrieveShowingRoomLayoutAPIView.as_view(), name='showing-room-layout'),
]
