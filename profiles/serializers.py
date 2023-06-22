from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """ This serializer is for the client facing profile.
    Clients cannot access the 'notes' field, which is meant
    for staff members only."""
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'is_owner',
            'name', 'image',
            'created_at', 'updated_at',
        ]


class ClientSerializer(serializers.ModelSerializer):
    """ This serializer is for the staff members facing profile.
    Staff members have access to 'notes' field.
    Staff members also cannot access the image, which is not
    relevant as staff member """
    owner = serializers.ReadOnlyField(source='owner.username')
    appointments_count = serializers.ReadOnlyField()
    has_appointments_today = serializers.ReadOnlyField()

    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'is_owner',
            'name', 'notes',
            'appointments_count', 'has_appointments_today',
            'created_at', 'updated_at',
        ]

class UserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = [
            'username',
            'is_staff',
        ]