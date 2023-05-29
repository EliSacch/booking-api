from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # To allow users to log in and out of API in-browser interface
    path('api_auth/', include('rest_framework.urls')),
    path('', include('profiles.urls')),
    path('', include('appointments.urls')),
    path('', include('services.urls')),
]
