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
    
class enterpriseModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
class location (models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"

# Create your models here.
