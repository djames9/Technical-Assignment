from django.urls import path
from .views import (
    SensorDataCreateView,
    SensorDataListView,
    SensorDataSummaryView,
)

urlpatterns = [
    # POST /api/v1/data/
    path("data/", SensorDataCreateView.as_view(), name="sensor-data-create"),

    # GET /api/v1/data/sensor/<sensor_id>/
    path(
        "data/sensor/<str:sensor_id>/",
        SensorDataListView.as_view(),
        name="sensor-data-list",
    ),

    # GET /api/v1/data/summary/?sensor_id=...
    path(
        "data/summary/",
        SensorDataSummaryView.as_view(),
        name="sensor-data-summary",
    ),
]
