from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Appointment

from datetime import date
from django.utils import timezone
from dateutil.relativedelta import relativedelta

import math


""" This function is used in all views to calculate the slots
reserved for a specific appointment, from the selected time """
def calculate_slots(start, duration):
    duration_range = int(duration / 50)
    start_time = start
    slots = []

    for slot in range(0,duration_range):
        slots += [start_time + (slot*50)]
    return slots

class AppointmentSerializer(serializers.ModelSerializer):
    """ Serializer for the appointment model. 
    All information are accessible to both client and staff members.
    Clients cannot select the owner, which will be set to 
    the logged in user automatically """
    owner = serializers.ReadOnlyField(source='owner.username')
    slots = serializers.ReadOnlyField()

    def validate(self, data):
        # Clients can book appointments for the following day or after.
        if data['date'] <= timezone.now().date():
            raise serializers.ValidationError("This date is not available.")
        
        # Check that appointment date is not in more than 6 months in the future
        #The following code is from stackoverflow - link in README
        six_months = date.today() + relativedelta(months=+6)
        # end of code from stackoverflow
        if data['date'] > six_months:
            raise serializers.ValidationError(f"We are currently taking appointments until {six_months}")
        
        # Check the weekday and block appointments for Sundays and Mondays
        if data['date'].weekday() == 6 or data['date'].weekday() == 0:
             raise serializers.ValidationError("Sorry, we are closed! We are open Tuesday to Saturday.")
        
        # Then we check if the slot is already occupied
        duration = data['service'].duration
        start_time = data['time']
        slots = calculate_slots(start_time, duration)

        # Retrieve all appointments for the same date, and with overlapping slots
        overlapping_appointment = Appointment.objects.filter(
            date=data["date"]).filter(slots__overlap=slots)

        # For PUT method, we also check that the overlapping appointment is not the one being edited
        if self.instance:
            current_appointment = self.instance.id
            overlapping_appointment = overlapping_appointment.exclude(pk=current_appointment)

        if overlapping_appointment.exists():
            raise serializers.ValidationError(f"This slot is not available.")
        
        return data

    class Meta:
        model = Appointment
        fields = [
            'id', 'owner', 'service',
            'date', 'time', 'slots', 'notes',
            'created_at', 'updated_at',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Appointment.objects.all(),
                fields=['date', 'time']
            )
        ]
    
    # The following code is from Stackoverflow - link in README
    def to_representation(self, instance):
        rep = super(AppointmentSerializer, self).to_representation(instance)
        rep['service'] = instance.service.title
        if rep['owner']:
            rep['owner'] = instance.owner.username
        return rep
    # End of code from


class ClientAppointmentSerializer(serializers.ModelSerializer):
    """ Serializer for the appointment model. 
    All information are accessible to both client and staff members.
    Staff members can select an existing user as owner
    or make appointments for unregistered users """
    slots = serializers.ReadOnlyField()

    def validate(self, data):
        # Check if owner is null, in that case we make name mandatory.
        if data['owner'] is None and data['client_name'] == "":
            raise serializers.ValidationError("Please, enter a name for unregistered users")
        
        # Check that appointment date is not in the past.
        if data['date'] < timezone.now().date():
            raise serializers.ValidationError("Appointment cannot be in the past")
        
        # Check that appointment date is not in more than 6 months in the future
        #The following code is from stackoverflow - link in README
        six_months = date.today() + relativedelta(months=+6)
        # end of code from stackoverflow
        if data['date'] > six_months:
            raise serializers.ValidationError(f"We are currently taking appointments until {six_months}")
        
        # Check the weekday and block appointments for Sundays and Mondays
        if data['date'].weekday() == 6 or data['date'].weekday() == 0:
             raise serializers.ValidationError("Sorry, we are closed! We are open Tuesday to Saturday.")
        
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
                raise serializers.ValidationError(
                     f"Sorry, it is not possible to book appointments before {hour}:{minutes} today"
                     )
        
        # Then we check if the slot is already occupied
        duration = data['service'].duration
        start_time = data['time']
        slots = calculate_slots(start_time, duration)

        # Retrieve all appointments for the same date, and with overlapping slots
        overlapping_appointment = Appointment.objects.filter(
            date=data["date"]).filter(slots__overlap=slots)
        # For PUT method, we also check that the overlapping appointment is not the one being edited
        if self.instance:
            current_appointment = self.instance.id
            overlapping_appointment = overlapping_appointment.exclude(pk=current_appointment)

        if overlapping_appointment.exists():
            raise serializers.ValidationError(f"This slot is not available.")
        
        return data

    class Meta:
        model = Appointment
        fields = [
            'id', 'owner', 'client_name', 'service',
            'date', 'time', 'slots', 'notes',
            'created_at', 'updated_at',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Appointment.objects.all(),
                fields=['date', 'time']
            )
        ]
    
    # The following code is from Stackoverflow - link in README
    def to_representation(self, instance):
        rep = super(ClientAppointmentSerializer, self).to_representation(instance)
        rep['service'] = instance.service.title
        if rep['owner']:
            rep['owner'] = instance.owner.username
        return rep
    # End of code from stackoverflow