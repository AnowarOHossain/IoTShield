"""Quick script to check database data"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iotshield_backend.settings')
django.setup()

from dashboard.models import Device, SensorData, Alert

# Check devices
devices = Device.objects.all()
print(f"📱 Devices: {devices.count()}")
for d in devices:
    print(f"  - {d.name} ({d.device_id}) - {'✅ Active' if d.is_active else '❌ Inactive'}")

# Check sensor data
readings = SensorData.objects.all()
print(f"\n📊 Sensor Readings: {readings.count()}")
if readings.exists():
    print("\nLatest 10 readings:")
    for s in readings.order_by('-timestamp')[:10]:
        anomaly = " ⚠️ ANOMALY" if s.is_anomaly else ""
        print(f"  {s.sensor_type}: {s.value}{s.unit} from {s.device.name}{anomaly}")

# Check alerts
alerts = Alert.objects.all()
print(f"\n🚨 Alerts: {alerts.count()}")
if alerts.exists():
    print("\nLatest 5 alerts:")
    for a in alerts.order_by('-created_at')[:5]:
        print(f"  [{a.severity}] {a.title}")
