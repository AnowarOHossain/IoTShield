"""
IoTShield Django Models
Database models for devices, sensors, alerts, and logs
"""
from django.db import models
from django.utils import timezone


class Device(models.Model):
    """IoT Device Model"""
    DEVICE_TYPES = [
        ('ESP32', 'ESP32 Microcontroller'),
        ('RASPBERRY_PI', 'Raspberry Pi'),
        ('SIMULATOR', 'Simulator'),
    ]
    
    device_id = models.CharField(max_length=100, unique=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.device_id})"


class SensorData(models.Model):
    """Sensor Reading Model"""
    SENSOR_TYPES = [
        ('TEMPERATURE', 'Temperature Sensor'),
        ('HUMIDITY', 'Humidity Sensor'),
        ('GAS', 'Gas Sensor'),
        ('FLAME', 'Flame Sensor'),
        ('MOTION', 'Motion Sensor'),
        ('LIGHT', 'Light Sensor'),
    ]
    
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='sensor_data')
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    value = models.FloatField()
    unit = models.CharField(max_length=20, blank=True)
    is_anomaly = models.BooleanField(default=False)
    anomaly_score = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['device', '-timestamp']),
            models.Index(fields=['sensor_type', '-timestamp']),
            models.Index(fields=['is_anomaly']),
        ]
    
    def __str__(self):
        return f"{self.sensor_type}: {self.value}{self.unit} @ {self.timestamp}"


class Alert(models.Model):
    """Alert Model for Anomaly Notifications"""
    SEVERITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('ACKNOWLEDGED', 'Acknowledged'),
        ('RESOLVED', 'Resolved'),
        ('IGNORED', 'Ignored'),
    ]
    
    sensor_data = models.ForeignKey(SensorData, on_delete=models.CASCADE, related_name='alerts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    ai_suggestion = models.TextField(blank=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['severity', 'status']),
        ]
    
    def __str__(self):
        return f"[{self.severity}] {self.title}"


class ControlCommand(models.Model):
    """Control Command Model for Actuation"""
    COMMAND_TYPES = [
        ('TURN_ON', 'Turn On'),
        ('TURN_OFF', 'Turn Off'),
        ('ADJUST', 'Adjust'),
        ('ALERT', 'Alert'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('EXECUTED', 'Executed'),
        ('FAILED', 'Failed'),
    ]
    
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='commands')
    command_type = models.CharField(max_length=20, choices=COMMAND_TYPES)
    parameters = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.command_type} -> {self.device.name} [{self.status}]"


class SystemLog(models.Model):
    """System Log Model"""
    LOG_LEVELS = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    level = models.CharField(max_length=10, choices=LOG_LEVELS)
    module = models.CharField(max_length=100)
    message = models.TextField()
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['level']),
        ]
    
    def __str__(self):
        return f"[{self.level}] {self.module}: {self.message[:50]}"
