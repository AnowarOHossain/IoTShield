"""
Django management command to test Gemini Anomaly Detection
"""
from django.core.management.base import BaseCommand
from iotshield_backend.gemini_anomaly_detector import GeminiAnomalyDetector
import json


class Command(BaseCommand):
    help = 'Test Gemini Anomaly Detection with sample sensor data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--sensor-type',
            type=str,
            default='TEMPERATURE',
            help='Sensor type to test (default: TEMPERATURE)'
        )
        parser.add_argument(
            '--value',
            type=float,
            default=45.5,
            help='Sensor value to test (default: 45.5)'
        )
    
    def handle(self, *args, **options):
        sensor_type = options['sensor_type']
        value = options['value']
        
        self.stdout.write(self.style.SUCCESS(f'\n=== Testing Gemini Anomaly Detector ===\n'))
        
        # Create test sensor data
        test_data = {
            'sensor_type': sensor_type,
            'value': value,
            'unit': self.get_unit(sensor_type),
            'device_name': 'Test Device',
            'location': 'Test Lab',
            'timestamp': '2025-10-31T12:00:00Z'
        }
        
        self.stdout.write(f'Test Data:')
        self.stdout.write(json.dumps(test_data, indent=2))
        
        # Initialize detector
        detector = GeminiAnomalyDetector()
        
        if not detector.model:
            self.stdout.write(self.style.ERROR('\nError: Gemini API not configured!'))
            self.stdout.write('Please set GEMINI_API_KEY in your .env file')
            return
        
        # Analyze with Gemini
        self.stdout.write(self.style.WARNING('\nCalling Gemini API...'))
        result = detector.analyze_with_gemini(test_data)
        
        # Display results
        self.stdout.write(self.style.SUCCESS('\n=== Analysis Results ===\n'))
        self.stdout.write(f'Anomaly: {result["anomaly"]}')
        self.stdout.write(f'Severity: {result["severity"]}')
        self.stdout.write(f'\nExplanation:\n{result["explanation"]}')
        self.stdout.write(f'\nSuggestion:\n{result["suggestion"]}')
        
        if result['anomaly']:
            self.stdout.write(self.style.ERROR('\n ANOMALY DETECTED!'))
        else:
            self.stdout.write(self.style.SUCCESS('\n Normal reading'))
        
        self.stdout.write('\n')
    
    def get_unit(self, sensor_type):
        """Get appropriate unit for sensor type"""
        units = {
            'TEMPERATURE': '°C',
            'HUMIDITY': '%',
            'GAS': 'ppm',
            'FLAME': 'level',
            'MOTION': 'detected',
            'LIGHT': 'lux'
        }
        return units.get(sensor_type, '')
