from django.urls import path
from allservices import views

urlpatterns = [
    path('services/', views.ServiceList.as_view()),
    path('view-services/', views.ClientFacingServiceList.as_view()),
    path('services/<int:pk>/', views.ServiceDetail.as_view()),
]