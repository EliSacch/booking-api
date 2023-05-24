from rest_framework import serializers
from .models import Appointment
from django.utils import timezone

import math


class AppointmentSerializer(serializers.ModelSerializer):
    """ Serializer for the appointment model. 
    All information are accessible to both client and staff members.
    Clients cannot select the owner, which will be set to 
    the logged in user automatically """
    owner = serializers.ReadOnlyField(source='owner.username')

    def validate(self, data):
        # Clients can book appointments for the following day or after.
        if data['date'] <= timezone.now().date():
            raise serializers.ValidationError("This date is not available.")

    class Meta:
        model = Appointment
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'date', 'time', 'notes',
        ]


class ClientAppointmentSerializer(serializers.ModelSerializer):
    """ Serializer for the appointment model. 
    All information are accessible to both client and staff members.
    Staff members can select an existing user as owner """

    def validate(self, data):
        # Check if owner is null, in that case we make name mandatory.
        if data['owner'] is None and data['client_name'] == "":
            raise serializers.ValidationError("Please, enter a name for unregistered users")
        
        # Check that appointment date is not in the past.
        if data['date'] < timezone.now().date():
            raise serializers.ValidationError("Appointment cannot be in the past")
        
        # If appointment is for today, check that time slot is not in the past
        if data['date'] == timezone.now().date():
            # This is the current hour rounded down
            current_time = (timezone.now().time().hour) * 100
            # Users cannot book for current hour, so we add 100
            first_available = current_time + 100
            # If the current time is in the second half of the hour,
            # we postpone the available spot of another half an hour
            if timezone.now().time().minute > 29:
                first_available += 50
            selected_slot = data['time']
            # Users cannot book any spot before the first available
            if selected_slot < first_available:
                hour = math.floor(first_available / 100)
                minutes = "00" if (first_available % 100) < 50 else "30"
                raise serializers.ValidationError(f"The first available spot for today is at {hour}:{minutes}")
        
        return data
    
        

    class Meta:
        model = Appointment
        fields = [
            'id', 'owner', 'client_name', 'created_at', 'updated_at',
            'date', 'time', 'notes',
        ]