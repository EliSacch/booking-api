from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """ This serializer is for the client facing profile.
    Clients cannot access the 'notes' field, which is meant
    for staff members only. Clients also cannot access 
    the 'isStaff' field """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'name', 'image',
        ]


class ClientSerializer(serializers.ModelSerializer):
    """ This serializer is for the staff members facing profile.
    Staff members have access to 'notes' and 'isStaff' fields.
    Staff members also cannot access the image, which is not
    relevant as staff member """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'name', 'notes', 'isStaff',
        ]