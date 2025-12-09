from django.urls import path
from .views import SensorDataCreateView, SensorDataListView

urlpatterns = [
    # POST /api/v1/data/
    path("data/", SensorDataCreateView.as_view(), name="sensor-data-create"),

    # GET /api/v1/data/sensor/<sensor_id>/?start=...&end=...
    path(
        "data/sensor/<str:sensor_id>/",
        SensorDataListView.as_view(),
        name="sensor-data-list",
    ),
]
