from datetime import timedelta
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.db import connection
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
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
    - If no start/end are provided, defaults to last 24 hours (from now backwards)
    """
    serializer_class = SensorDataSerializer

    def get_queryset(self):
        sensor_id = self.kwargs["sensor_id"]
        qs = SensorData.objects.filter(sensor_id=sensor_id)

        start_str = self.request.query_params.get("start")
        end_str = self.request.query_params.get("end")

        now = timezone.now()

        # default: last 24 hours
        if not start_str and not end_str:
            start = now - timedelta(hours=24)
            return qs.filter(timestamp__gte=start).order_by("timestamp")

        # custom range
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
            queryset = qs.filter(timestamp__gte=start, timestamp__lte=end)
        else:
            queryset = qs.filter(timestamp__gte=start)

        return queryset.order_by("timestamp")


class SensorDataSummaryView(APIView):
    """
    GET /api/v1/data/summary/?sensor_id=...&start=...&end=...

    Returns hourly averages using TimescaleDB time_bucket().
    Default: last 7 days.
    """

    def get(self, request, *args, **kwargs):
        sensor_id = request.query_params.get("sensor_id")
        if not sensor_id:
            raise ValidationError({"sensor_id": "This query parameter is required."})

        start_str = request.query_params.get("start")
        end_str = request.query_params.get("end")

        now = timezone.now()

        # Parse end or default = now
        if end_str:
            end = parse_datetime(end_str)
            if end is None:
                raise ValidationError({"end": "Invalid datetime format. Use ISO 8601."})
        else:
            end = now

        # Parse start or default = last 7 days
        if start_str:
            start = parse_datetime(start_str)
            if start is None:
                raise ValidationError({"start": "Invalid datetime format. Use ISO 8601."})
        else:
            start = end - timedelta(days=7)

        query = """
            SELECT
                time_bucket('1 hour', timestamp) AS bucket,
                AVG(soil_moisture) AS avg_soil_moisture,
                AVG(temperature) AS avg_temperature,
                AVG(precipitation) AS avg_precipitation
            FROM analytics_sensordata
            WHERE sensor_id = %s
              AND timestamp >= %s
              AND timestamp < %s
            GROUP BY bucket
            ORDER BY bucket;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [sensor_id, start, end])
            rows = cursor.fetchall()

        data = [
            {
                "bucket": row[0].isoformat(),
                "avg_soil_moisture": float(row[1]) if row[1] is not None else None,
                "avg_temperature": float(row[2]) if row[2] is not None else None,
                "avg_precipitation": float(row[3]) if row[3] is not None else None,
            }
            for row in rows
        ]

        return Response(data)


# Create your views here.
