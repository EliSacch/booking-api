from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # To allow users to log in and out of API in-browser interface
    path('api_auth/', include('rest_framework.urls')),
    # To use dj-rest-auth
    path('dj-rest-auth/', include('rest_framework.urls')),
    path(
        'dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')
    ),
    path('', include('profiles.urls')),
    path('', include('appointments.urls')),
    path('', include('services.urls')),
]
