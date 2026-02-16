"""
TinyLlama-Based Anomaly Detection Test
This script helps verify the TinyLlama detector works correctly
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iotshield_backend.settings')
django.setup()

from iotshield_backend.tinylama_anomaly_detector import TinyLlamaAnomalyDetector
from dashboard.models import SensorData
from datetime import datetime, timezone

def test_tinylama_detector():
	"""Test the new TinyLlama-based anomaly detector"""
	print("\n" + "="*60)
	print("TINYLAMA ANOMALY DETECTOR TEST")
	print("="*60 + "\n")
    
	detector = TinyLlamaAnomalyDetector()
    
	# Test cases
	test_cases = [
		{
			'name': 'Normal Temperature',
			'data': {
				'sensor_type': 'TEMPERATURE',
				'value': 22.5,
				'unit': '°C',
				'device_name': 'Living Room Sensor',
				'location': 'Living Room',
				'timestamp': datetime.now(timezone.utc).isoformat()
			}
		},
		{
			'name': 'High Temperature (Anomaly)',
			'data': {
				'sensor_type': 'TEMPERATURE',
				'value': 48.3,
				'unit': '°C',
				'device_name': 'Kitchen Sensor',
				'location': 'Kitchen',
				'timestamp': datetime.now(timezone.utc).isoformat()
			}
		},
		{
			'name': 'Normal Humidity',
			'data': {
				'sensor_type': 'HUMIDITY',
				'value': 45.0,
				'unit': '%',
				'device_name': 'Bedroom Sensor',
				'location': 'Bedroom',
				'timestamp': datetime.now(timezone.utc).isoformat()
			}
		},
		{
			'name': 'Gas Leak (Critical Anomaly)',
			'data': {
				'sensor_type': 'GAS',
				'value': 0.75,
				'unit': 'ppm',
				'device_name': 'Kitchen Sensor',
				'location': 'Kitchen',
				'timestamp': datetime.now(timezone.utc).isoformat()
			}
		}
	]
    
	for i, test_case in enumerate(test_cases, 1):
		print(f"\n{'='*60}")
		print(f"Test Case {i}: {test_case['name']}")
		print(f"{'='*60}")
        
		print(f"\nInput:")
		print(f"  Sensor: {test_case['data']['sensor_type']}")
		print(f"  Value: {test_case['data']['value']} {test_case['data']['unit']}")
		print(f"  Location: {test_case['data']['location']}")
        
		print(f"\nCalling TinyLlama...")
		result = detector.analyze(test_case['data'])
        
		print(f"\nResults:")
		print(f"  Anomaly: {' YES' if result['anomaly'] else ' NO'}")
		print(f"  Severity: {result['severity']}")
		print(f"  Explanation: {result['explanation']}")
		print(f"  Suggestion: {result['suggestion']}")
    
	print(f"\n{'='*60}")
	print("ALL TESTS COMPLETED")
	print(f"{'='*60}\n")

def test_with_recent_data():
	"""Test with recent sensor data from database"""
	print("\n" + "="*60)
	print("TESTING WITH RECENT DATABASE RECORDS")
	print("="*60 + "\n")
    
	# Get recent sensor data
	recent_data = SensorData.objects.order_by('-timestamp')[:5]
    
	if not recent_data:
		print("No sensor data found in database.\n")
		return
    
	detector = TinyLlamaAnomalyDetector()
    
	print(f"Found {len(recent_data)} recent sensor readings\n")
    
	for i, sensor_data in enumerate(recent_data, 1):
		print(f"\n{'='*60}")
		print(f"Record {i}")
		print(f"{'='*60}")
        
		print(f"\nSensor Data:")
		print(f"  Type: {sensor_data.sensor_type}")
		print(f"  Value: {sensor_data.value} {sensor_data.unit}")
		print(f"  Device: {sensor_data.device.name}")
		print(f"  Location: {sensor_data.device.location}")
		print(f"  Timestamp: {sensor_data.timestamp}")
        
		# Prepare data dict
		data_dict = {
			'sensor_type': sensor_data.sensor_type,
			'value': sensor_data.value,
			'unit': sensor_data.unit,
			'device_name': sensor_data.device.name,
			'location': sensor_data.device.location,
			'timestamp': sensor_data.timestamp.isoformat()
		}
        
		print(f"\nAnalyzing...")
		result = detector.analyze(data_dict)
        
		print(f"\nTinyLlama Analysis:")
		print(f"  Anomaly: {' YES' if result['anomaly'] else ' NO'}")
		print(f"  Severity: {result['severity']}")
		print(f"  Explanation: {result['explanation']}")
		print(f"  Suggestion: {result['suggestion']}")
        
		if sensor_data.is_anomaly:
			print(f"\n  Previous Detection: ANOMALY (score: {sensor_data.anomaly_score:.2f})")
		else:
			print(f"\n  Previous Detection: NORMAL")
    
	print(f"\n{'='*60}\n")

if __name__ == '__main__':
	import argparse
    
	parser = argparse.ArgumentParser(description='Test TinyLlama Anomaly Detector')
	parser.add_argument(
		'--mode',
		choices=['test', 'recent', 'both'],
		default='both',
		help='Test mode: test=predefined cases, recent=database records, both=all'
	)
    
	args = parser.parse_args()
    
	if args.mode in ['test', 'both']:
		test_tinylama_detector()
    
	if args.mode in ['recent', 'both']:
		test_with_recent_data()
    
	print("\nTest script completed!\n")
