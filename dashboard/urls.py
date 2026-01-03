"""Dashboard URL Configuration"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Authentication views
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard views
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('devices/', views.devices, name='devices'),
    path('alerts/', views.alerts, name='alerts'),
    
    # API endpoints
    path('api/sensors/data/', views.api_sensor_data, name='api_sensor_data'),
    path('api/alerts/list/', views.api_alerts_list, name='api_alerts_list'),
    path('api/devices/list/', views.api_devices_list, name='api_devices_list'),
    path('api/stats/summary/', views.api_stats_summary, name='api_stats_summary'),
    path('api/control/command/', views.api_send_control_command, name='api_control_command'),
]
