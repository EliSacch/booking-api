from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Appointment
from django.contrib.auth.models import User
from treatments.models import Treatment

from datetime import date
from django.utils import timezone
from dateutil.relativedelta import relativedelta

import math


class BaseAppointmentSerializer(serializers.ModelSerializer):
    """ Base Serializer for the appointment model. 
    It will be user as blueprint for the two 
    client or staff facing serializers """
    treatment = serializers.ChoiceField(choices=Treatment.objects.filter(is_active=True))
    end_time = serializers.ReadOnlyField()
    status = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_status(self, obj):
        return 'Past' if obj.date < date.today() else 'Today' if obj.date == date.today() else 'Upcoming'

    def validate(self, data):
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
        
        # Find the time range (start_time - end_time) for the current instance
        duration = 50
        if data['treatment']:
            duration = data['treatment'].duration
        start_time = data['time']
        end_time = start_time+duration

        #Check that end-time is not after closing time (17:00)
        if end_time > 1700:
            raise serializers.ValidationError(f"This appointment is too late")

        # Retrieve all appointments for the same date
        same_day_appointments = Appointment.objects.filter(date=data["date"])
        # For PUT method, exclude the current instance from the queryset
        if self.instance:
            current_appointment = self.instance.id
            same_day_appointments = same_day_appointments.exclude(pk=current_appointment)

        # For each appointment in the queryset, check that the instance appointment time range
        # does not have overlapping time with another appoint range (start_time - end_time)
        for appointment in same_day_appointments:
            # The following code is from Stackoverflow - Link in README
            overlapping = range(max(start_time, appointment.time), min(end_time, appointment.end_time))
            # End of code from Stackoverflow
            if len(overlapping) != 0:
                raise serializers.ValidationError(f"This time is not available.")
        
        return data


    class Meta:
        model = Appointment
        fields = [
            'id', 'owner', 'is_owner',
            'treatment', 
            'status',
            'date', 'time', 'notes',
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
        rep = super(BaseAppointmentSerializer, self).to_representation(instance)
        if rep['treatment']:
            rep['treatment'] = instance.treatment.title
        return rep
    # End of code from


class ClientAppointmentSerializer(BaseAppointmentSerializer):
    """ Client facing serializer.. 
    Clients cannot select the owner, which will be set to 
    the logged in user automatically """
    owner = serializers.ReadOnlyField(source='owner.username')
    
    def validate(self, data):
        # Clients can book appointments for the following day or after.
        if data['date'] <= timezone.now().date():
            raise serializers.ValidationError("This date is not available.")
        
        return super().validate(data)


class StaffAppointmentSerializer(BaseAppointmentSerializer):
    """ Staff facing serializer.
    Staff members can select an existing user as owner
    or make appointments for unregistered users """
    owner_username = serializers.ReadOnlyField(source='owner.username')

    def validate(self, data):
        # Check if owner is null, in that case we make name mandatory.
        if data['owner'] is None and data['client_name'] == "":
            raise serializers.ValidationError("Please, enter a name for unregistered users")
        
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

        return super().validate(data)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'owner', 'owner_username',
            'client_name', 
            'treatment', 
            'status',
            'date', 'time', 'end_time', 'notes',
            'created_at', 'updated_at',
        ]
