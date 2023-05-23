from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    """ Serializer for the appointment model. 
    All information are accessible to both client and staff members """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Appointment
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'date', 'notes',
        ]
