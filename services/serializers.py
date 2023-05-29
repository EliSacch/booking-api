from rest_framework import serializers
from .models import Service

from datetime import date
from django.utils import timezone
from dateutil.relativedelta import relativedelta

import math


class ServiceSerializer(serializers.ModelSerializer):
    """ Serializer for the service model. 
    All information are accessible to staff members only """
    DURATION_CHOICES = [
        (50, '00:30'),
        (100, '01:00'),
        (150, '01:30'),
        (200, '02:00'),
        (250, '02:30'),
        (300, '03:00'),
        (350, '03:30'),
        (400, '04:00'),
        (450, '04:30'),
        (500, '05:00'),
        (550, '05:30'),
        (600, '06:00'),
        (650, '06:30'),
        (700, '07:00'),
        (750, '07:30'),
    ]
    duration = serializers.ChoiceField(choices=DURATION_CHOICES)


    class Meta:
        model = Service
        fields = [
            'id', 'title', 'description',
            'price', 'duration', 'image',
        ]
