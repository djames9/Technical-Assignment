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
    serializer_class = SensorDataSerializer

    def get_queryset(self):
        sensor_id = self.kwargs["sensor_id"]
        qs = SensorData.objects.filter(sensor_id=sensor_id)

        start_str = self.request.query_params.get("start")
        end_str = self.request.query_params.get("end")

        from datetime import timedelta
        from django.utils import timezone
        from django.utils.dateparse import parse_datetime
        from rest_framework.exceptions import ValidationError

        now = timezone.now()

        if start_str or end_str:
            if start_str:
                start = parse_datetime(start_str)
                if start is None:
                    raise ValidationError({"start": "Invalid datetime format. Use ISO 8601."})
            else:
                start = now - timedelta(hours=24)

            if end_str:
                end = parse_datetime(end_str)
                if end is None:
                    raise ValidationError({"end": "Invalid datetime format. Use ISO 8601."})
                qs = qs.filter(timestamp__gte=start, timestamp__lte=end)
            else:
                qs = qs.filter(timestamp__gte=start)
        else:
            # Default: last 24 hours, but allow future records
            start = now - timedelta(hours=24)
            qs = qs.filter(timestamp__gte=start)

        return qs.order_by("timestamp")



# Create your views here.
