# analytics/views.py
from datetime import timedelta
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .models import SensorData
from .serializers import SensorDataSerializer


class SensorDataCreateView(generics.CreateAPIView):
    """
    POST /api/v1/data/
    Accepts a single sensor data point and saves it.
    """
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer


class SensorDataListView(generics.ListAPIView):
    """
    GET /api/v1/data/sensor/<sensor_id>/?start=...&end=...
    - Returns raw data points for a given sensor_id
    - If no start/end are provided, defaults to last 24 hours
    """
    serializer_class = SensorDataSerializer

    def get_queryset(self):
        sensor_id = self.kwargs["sensor_id"]

        # Base queryset for this sensor
        qs = SensorData.objects.filter(sensor_id=sensor_id)

        # Query params: ?start=...&end=...
        start_str = self.request.query_params.get("start")
        end_str = self.request.query_params.get("end")

        now = timezone.now()

        if start_str or end_str:
            # Parse datetimes if provided
            if start_str:
                start = parse_datetime(start_str)
                if start is None:
                    raise ValidationError({"start": "Invalid datetime format. Use ISO 8601."})
            else:
                # no start => default to 24h before end or now
                end_tmp = parse_datetime(end_str) or now
                start = end_tmp - timedelta(hours=24)

            if end_str:
                end = parse_datetime(end_str)
                if end is None:
                    raise ValidationError({"end": "Invalid datetime format. Use ISO 8601."})
            else:
                end = now
        else:
            # Default: last 24 hours
            end = now
            start = now - timedelta(hours=24)

        return qs.filter(timestamp__gte=start, timestamp__lte=end).order_by("timestamp")


# Create your views here.
