from django.contrib import admin
from dashboard.models import Device, SensorData, Alert, ControlCommand, SystemLog


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'name', 'device_type', 'location', 'is_active', 'last_seen')
    list_filter = ('device_type', 'is_active')
    search_fields = ('device_id', 'name', 'location')
    date_hierarchy = 'created_at'


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('device', 'sensor_type', 'value', 'unit', 'is_anomaly', 'timestamp')
    list_filter = ('sensor_type', 'is_anomaly', 'timestamp')
    search_fields = ('device__name', 'sensor_type')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'status', 'created_at')
    list_filter = ('severity', 'status', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ControlCommand)
class ControlCommandAdmin(admin.ModelAdmin):
    list_display = ('device', 'command_type', 'status', 'created_at')
    list_filter = ('command_type', 'status', 'created_at')
    search_fields = ('device__name',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'executed_at')


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('level', 'module', 'message', 'timestamp')
    list_filter = ('level', 'module', 'timestamp')
    search_fields = ('module', 'message')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)
