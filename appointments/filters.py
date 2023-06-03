from rest_framework import filters
from django_filters import rest_framework as filters
from django import forms

from .models import Appointment

from datetime import date as d
 
# Appoinment filters
class AppointmentFilter(filters.FilterSet):
    
    date = filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}, format='%Y/%M/%D'))
    
    class Meta:
        model = Appointment
        fields = ['date',]



