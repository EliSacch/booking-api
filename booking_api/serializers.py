from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')
    profile_name = serializers.ReadOnlyField(source='profile.name')
    profile_notes = serializers.ReadOnlyField(source='profile.notes')
    is_staff = serializers.SerializerMethodField()

    def get_is_staff(self, obj):
        return obj.is_staff

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + \
            ( 'profile_id', 'profile_image', 'profile_name',
             'profile_notes', 'is_staff' )
