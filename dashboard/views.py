"""Dashboard views for IoTShield"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg
import json

from dashboard.models import Device, SensorData, Alert, ControlCommand, SystemLog
from iotshield_backend.mqtt_client import mqtt_client


def index(request):
    """Landing page"""
    return render(request, 'dashboard.html')


def dashboard(request):
    """Main dashboard view"""
    # Get recent statistics
    total_devices = Device.objects.filter(is_active=True).count()
    total_alerts = Alert.objects.filter(status='NEW').count()
    recent_readings = SensorData.objects.count()
    
    # Get recent alerts
    recent_alerts = Alert.objects.all()[:10]
    
    context = {
        'total_devices': total_devices,
        'total_alerts': total_alerts,
        'recent_readings': recent_readings,
        'recent_alerts': recent_alerts,
    }
    
    return render(request, 'dashboard.html', context)


def devices(request):
    """Devices list view"""
    devices_list = Device.objects.all().order_by('-last_seen')
    
    context = {
        'devices': devices_list,
    }
    
    return render(request, 'devices.html', context)


def alerts(request):
    """Alerts list view"""
    alerts_list = Alert.objects.all().order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        alerts_list = alerts_list.filter(status=status)
    
    context = {
        'alerts': alerts_list,
    }
    
    return render(request, 'alerts.html', context)


# API Views

def api_sensor_data(request):
    """API: Get sensor data"""
    hours = int(request.GET.get('hours', 24))
    sensor_type = request.GET.get('sensor_type', None)
    device_id = request.GET.get('device_id', None)
    
    cutoff_time = timezone.now() - timedelta(hours=hours)
    
    queryset = SensorData.objects.filter(timestamp__gte=cutoff_time)
    
    if sensor_type:
        queryset = queryset.filter(sensor_type=sensor_type)
    
    if device_id:
        queryset = queryset.filter(device__device_id=device_id)
    
    data = []
    for reading in queryset.order_by('timestamp'):
        data.append({
            'timestamp': reading.timestamp.isoformat(),
            'sensor_type': reading.sensor_type,
            'value': reading.value,
            'unit': reading.unit,
            'device_id': reading.device.device_id,
            'is_anomaly': reading.is_anomaly,
            'anomaly_score': reading.anomaly_score,
        })
    
    return JsonResponse({'data': data})


def api_alerts_list(request):
    """API: Get alerts list"""
    status = request.GET.get('status', None)
    severity = request.GET.get('severity', None)
    limit = int(request.GET.get('limit', 50))
    
    queryset = Alert.objects.all()
    
    if status:
        queryset = queryset.filter(status=status)
    
    if severity:
        queryset = queryset.filter(severity=severity)
    
    alerts = []
    for alert in queryset.order_by('-created_at')[:limit]:
        alerts.append({
            'id': alert.id,
            'title': alert.title,
            'description': alert.description,
            'ai_suggestion': alert.ai_suggestion,
            'severity': alert.severity,
            'status': alert.status,
            'sensor_type': alert.sensor_data.sensor_type,
            'device_name': alert.sensor_data.device.name,
            'created_at': alert.created_at.isoformat(),
        })
    
    return JsonResponse({'alerts': alerts})


def api_devices_list(request):
    """API: Get devices list"""
    devices = []
    
    for device in Device.objects.all():
        # Get recent statistics
        recent_data = SensorData.objects.filter(
            device=device,
            timestamp__gte=timezone.now() - timedelta(hours=24)
        )
        
        devices.append({
            'device_id': device.device_id,
            'name': device.name,
            'type': device.device_type,
            'location': device.location,
            'is_active': device.is_active,
            'last_seen': device.last_seen.isoformat(),
            'total_readings_24h': recent_data.count(),
            'anomalies_24h': recent_data.filter(is_anomaly=True).count(),
        })
    
    return JsonResponse({'devices': devices})


def api_stats_summary(request):
    """API: Get summary statistics"""
    # Time period
    hours = int(request.GET.get('hours', 24))
    cutoff_time = timezone.now() - timedelta(hours=hours)
    
    # Overall stats
    total_devices = Device.objects.filter(is_active=True).count()
    total_readings = SensorData.objects.filter(timestamp__gte=cutoff_time).count()
    total_anomalies = SensorData.objects.filter(
        timestamp__gte=cutoff_time,
        is_anomaly=True
    ).count()
    
    # Alerts by severity
    alerts_by_severity = Alert.objects.filter(
        created_at__gte=cutoff_time
    ).values('severity').annotate(count=Count('id'))
    
    # Sensor type statistics
    sensor_stats = SensorData.objects.filter(
        timestamp__gte=cutoff_time
    ).values('sensor_type').annotate(
        avg_value=Avg('value'),
        count=Count('id'),
        anomalies=Count('id', filter=models.Q(is_anomaly=True))
    )
    
    summary = {
        'total_devices': total_devices,
        'total_readings': total_readings,
        'total_anomalies': total_anomalies,
        'anomaly_rate': (total_anomalies / total_readings * 100) if total_readings > 0 else 0,
        'alerts_by_severity': list(alerts_by_severity),
        'sensor_stats': list(sensor_stats),
        'period_hours': hours,
    }
    
    return JsonResponse(summary)


@csrf_exempt
def api_send_control_command(request):
    """API: Send control command to device"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        device_id = data.get('device_id')
        command_type = data.get('command_type')
        parameters = data.get('parameters', {})
        
        # Get device
        device = Device.objects.get(device_id=device_id)
        
        # Create control command
        command = ControlCommand.objects.create(
            device=device,
            command_type=command_type,
            parameters=parameters
        )
        
        # Publish to MQTT
        success = mqtt_client.publish_control_command(command)
        
        if success:
            return JsonResponse({
                'success': True,
                'command_id': command.id,
                'message': 'Command sent successfully'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Failed to send command'
            }, status=500)
    
    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
