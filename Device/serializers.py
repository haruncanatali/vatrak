from rest_framework import serializers
from Device.models import Devices


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = ('id', 'name', 'battery', 'locked', 'last_locked_date', 'last_unlocked_date')
