from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

docs_urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(docs_urlpatterns)),
    path('api/', include('users.urls', namespace='users')),
    path('api/', include('movies.urls', namespace='movies')),
    path('api/', include('theaters.urls', namespace='theaters')),
    path('api/', include('showings.urls', namespace='showings')),
    path('api/', include('reservations.urls', namespace='reservations')),
    path('api/', include('payments.urls', namespace='payments')),
]
