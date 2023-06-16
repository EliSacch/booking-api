from django.contrib import admin
from django.urls import path, include
from .views import root_route, logout_route

urlpatterns = [
    path('admin/', admin.site.urls),
    # root
    path('', root_route),
    # To allow users to log in and out of API in-browser interface
    path('api_auth/', include('rest_framework.urls')),
    # custom logout route
    path('dj-rest-auth/logout/', logout_route),
    # To use dj-rest-auth
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path(
        'dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')
    ),
    path('', include('profiles.urls')),
    path('', include('appointments.urls')),
    path('', include('treatments.urls')),
]
