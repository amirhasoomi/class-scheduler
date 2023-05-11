from rest_framework import serializers
from .models import Schedule, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name',)


class ScheduleSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Schedule
        fields = ('name', 'location')

    def validate(self, attrs):
        # username = attrs['username'].lower()
        # if Profile.objects.filter(username=username).exists():
        #     raise serializers.ValidationError(
        #         dict(username=['username is used before!', ]))
        # if Profile.objects.filter(mobile=attrs['mobile']).exists():
        #     raise serializers.ValidationError(
        #         dict(mobile=['mobile is used before!', ]))
        # if Profile.objects.filter(email=attrs['email']).exists():
        #     raise serializers.ValidationError(
        #         dict(email=['email is used before!', ]))
        return attrs
