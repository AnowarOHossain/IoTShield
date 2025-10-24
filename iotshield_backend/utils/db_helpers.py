"""Database helper utilities for IoTShield"""

from django.db.models import Avg, Max, Min, Count
from django.utils import timezone
from datetime import timedelta


def get_device_statistics(device):
    """Get statistics for a specific device"""
    from iotshield_backend.models import SensorData
    
    stats = SensorData.objects.filter(device=device).aggregate(
        total_readings=Count('id'),
        anomalies=Count('id', filter=models.Q(is_anomaly=True))
    )
    
    return stats


def get_sensor_stats_by_type(sensor_type, hours=24):
    """Get statistics for a sensor type over time period"""
    from iotshield_backend.models import SensorData
    
    cutoff_time = timezone.now() - timedelta(hours=hours)
    
    stats = SensorData.objects.filter(
        sensor_type=sensor_type,
        timestamp__gte=cutoff_time
    ).aggregate(
        avg=Avg('value'),
        max=Max('value'),
        min=Min('value'),
        count=Count('id')
    )
    
    return stats


def cleanup_old_data(days=30):
    """Remove sensor data older than specified days"""
    from iotshield_backend.models import SensorData, SystemLog
    
    cutoff_date = timezone.now() - timedelta(days=days)
    
    deleted_sensors = SensorData.objects.filter(timestamp__lt=cutoff_date).delete()
    deleted_logs = SystemLog.objects.filter(timestamp__lt=cutoff_date).delete()
    
    return {
        'sensor_data_deleted': deleted_sensors[0],
        'logs_deleted': deleted_logs[0]
    }
