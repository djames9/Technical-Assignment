Project Notes & Usage Instructions

This project already uses TimescaleDB through the Docker image:

timescale/timescaledb:latest-pg16


I also added a custom migration file called 002_make_sensordata_hypertable, which automatically converts the SensorData table into a hypertable during migration.
Because of this, you do not need to manually run makemigrations — the project is ready to start immediately.

How to Start the Project

Simply run:

docker compose up -d


Once the containers are running, you can test the API using the following links:

1. GET raw sensor data
http://localhost:8000/api/v1/data/sensor/<sensor_name>


Example:

http://localhost:8000/api/v1/data/sensor/sensor-01

2. POST new sensor data
http://localhost:8000/api/v1/data/

3. GET aggregated summary (hourly averages)
http://localhost:8000/api/v1/data/summary/?sensor_id=<sensor_name>


Example:

http://localhost:8000/api/v1/data/summary/?sensor_id=sensor-002

Example cURL Commands
POST example
curl -X POST http://localhost:8000/api/v1/data/ \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2025-12-09T10:30:00Z",
    "sensor_id": "sensor-001",
    "soil_moisture": 45.7,
    "temperature": 18.3,
    "precipitation": 2.4
  }'

GET raw data (last 24h)
curl "http://localhost:8000/api/v1/data/sensor/sensor-001/"

GET raw data with custom range
curl "http://localhost:8000/api/v1/data/sensor/sensor-001/?start=2000-01-01T00:00:00Z&end=2100-01-01T00:00:00Z"

GET hourly summary
curl "http://localhost:8000/api/v1/data/summary/?sensor_id=sensor-001"

Scalability Commentary

This application incorporates several architectural choices that prepare it for real-world, production-grade scalability—especially for time-series workloads:

1. TimescaleDB Hypertable

The SensorData table is automatically converted into a TimescaleDB hypertable via migration.
This provides:

faster inserts

efficient time-window queries

native aggregation using time_bucket()

2. Containerized Infrastructure

The entire system runs using Docker containers, including:

Django API service

TimescaleDB service

Grafana monitoring service

This architecture makes the system ready for cloud deployment and easy horizontal scaling.

3. Real-Time Monitoring in Grafana

Grafana is fully connected to TimescaleDB, allowing you to visualize data in real time.

To access Grafana:

Open: http://localhost:3000/

Username: admin

Password: admin123

Then:

Go to Connections → Data Sources

Choose PostgreSQL

Enter the database connection details

Once added, you can explore and visualize the data instantly.

I implemented a check to ensure that the application waits for the database to fully start before executing any commands.