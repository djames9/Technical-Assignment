from rest_framework import serializers
from .models import SensorData

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = [
            "timestamp",
            "sensor_id",
            "soil_moisture",
            "temperature",
            "precipitation",
        ]
