from django.urls import path
from treatments import views

urlpatterns = [
    path('treatments/', views.TreatmentList.as_view()),
    path('treatments/<int:pk>/', views.TreatmentDetail.as_view()),
]
