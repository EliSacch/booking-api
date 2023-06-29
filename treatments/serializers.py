from rest_framework import serializers
from .models import Treatment


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


class TreatmentSerializer(serializers.ModelSerializer):
    """ Serializer for the treatment model.
    All information are accessible to staff members only """

    duration = serializers.ChoiceField(choices=DURATION_CHOICES)

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

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('The price cannot be negative')
        return value

    class Meta:
        model = Treatment
        fields = [
            'id', 'title', 'description',
            'price', 'duration', 'image',
            'is_active', 'created_at', 'updated_at',
        ]


class ClientFacingTreatmentSerializer(serializers.ModelSerializer):
    """ Serializer for the treatment model.
    The following information are accessible to clients """
    class Meta:
        model = Treatment
        fields = [
            'id', 'title', 'description',
            'price', 'duration', 'image',
            'is_active',
        ]
