from django.urls import path
from appointments import views

urlpatterns = [
    path('appointments/', views.AppointmentList.as_view()),
    path('appointments/<int:pk>/', views.ClientAppointmentDetail.as_view()),
    path('my-appointments/', views.MyAppointmentList.as_view()),
    path('my-appointments/<int:pk>/', views.AppointmentDetail.as_view()),
]