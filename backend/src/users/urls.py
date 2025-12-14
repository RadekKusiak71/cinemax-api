from django.urls import path

from users.views import RegisterUserView, TokenObtainPairView, TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]