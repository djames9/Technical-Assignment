from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("analytics", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- 1) Enable TimescaleDB extension
                CREATE EXTENSION IF NOT EXISTS timescaledb;

                -- 2) Convert analytics_sensordata into a hypertable on "timestamp"
                SELECT create_hypertable(
                    'analytics_sensordata',
                    'timestamp',
                    if_not_exists => TRUE,
                    migrate_data  => TRUE
                );
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
