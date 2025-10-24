"""
Django Management Command to run MQTT listener
"""
from django.core.management.base import BaseCommand
from iotshield_backend.mqtt_client import mqtt_client
import time


class Command(BaseCommand):
    help = 'Start MQTT listener for IoTShield'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("""
╔══════════════════════════════════════════════════════╗
║       IoTShield MQTT Listener Started               ║
║   Listening for sensor data and control commands    ║
╚══════════════════════════════════════════════════════╝
        """))
        
        try:
            # Connect to MQTT broker
            mqtt_client.connect()
            
            self.stdout.write(self.style.SUCCESS('✓ MQTT listener is running'))
            self.stdout.write(self.style.WARNING('Press Ctrl+C to stop'))
            
            # Keep running
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nStopping MQTT listener...'))
            mqtt_client.disconnect()
            self.stdout.write(self.style.SUCCESS('✓ MQTT listener stopped'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            mqtt_client.disconnect()
