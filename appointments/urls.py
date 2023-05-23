from django.urls import path
from appointments import views

urlpatterns = [
    path('appointments/', views.AllAppointmentList.as_view()),
    path('appointments/<int:pk>/', views.AppointmentDetail.as_view()),
    path('my-appointments/', views.MyAppointmentList.as_view()),
    path('my-appointments/<int:pk>/', views.AppointmentDetail.as_view()),
]