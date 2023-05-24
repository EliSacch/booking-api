from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    """ Serializer for the appointment model. 
    All information are accessible to both client and staff members.
    Clients cannot select the owner, which will be set to 
    the logged in user automatically """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Appointment
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'date', 'notes',
        ]


class ClientAppointmentSerializer(serializers.ModelSerializer):
    """ Serializer for the appointment model. 
    All information are accessible to both client and staff members.
    Staff members can select an existing user as owner """

    def validate(self, data):
        """
        Check if owner is null, in that case we make name mandatory.
        """
        if data['owner'] is None and data['client_name'] == "":
            raise serializers.ValidationError("Please, enter a name for unregistered users")
        return data

    class Meta:
        model = Appointment
        fields = [
            'id', 'owner', 'client_name', 'created_at', 'updated_at',
            'date', 'notes',
        ]