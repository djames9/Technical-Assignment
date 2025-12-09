from django.db import models
from django.utils import timezone


class SensorData(models.Model):
    timestamp = models.DateTimeField(
        primary_key=True,
        default=timezone.now,
    )
    sensor_id = models.CharField(max_length=100)
    soil_moisture = models.FloatField()
    temperature = models.FloatField()
    precipitation = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["sensor_id", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.sensor_id} @ {self.timestamp}"

# Create your models here.
