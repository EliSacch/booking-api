from django.urls import path
from profiles import views

urlpatterns = [
    path('clients/', views.ProfileList.as_view()),
    path('clients/<int:pk>/', views.ClientProfileDetail.as_view()),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
]