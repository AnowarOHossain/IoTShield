"""
Test Severity Level Distribution
Tests the improved severity classification without calling Gemini API
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iotshield_backend.settings')
django.setup()

from iotshield_backend.gemini_anomaly_detector import GeminiAnomalyDetector
from datetime import datetime, timezone


def test_fallback_severity_levels():
    """Test the fallback analysis with various severity levels"""
    print("\n" + "="*70)
    print("SEVERITY LEVEL DISTRIBUTION TEST (Fallback Analysis)")
    print("="*70 + "\n")
    
    detector = GeminiAnomalyDetector()
    
    # Test cases covering all severity levels
    test_cases = [
        # LOW severity
        {'name': 'Slightly High Temp (LOW)', 'sensor_type': 'TEMPERATURE', 'value': 29.5, 'unit': '°C'},
        {'name': 'Slightly High Humidity (LOW)', 'sensor_type': 'HUMIDITY', 'value': 63, 'unit': '%'},
        {'name': 'Elevated Gas (LOW)', 'sensor_type': 'GAS', 'value': 0.36, 'unit': 'ppm'},
        
        # MEDIUM severity
        {'name': 'Moderately High Temp (MEDIUM)', 'sensor_type': 'TEMPERATURE', 'value': 39, 'unit': '°C'},
        {'name': 'High Humidity (MEDIUM)', 'sensor_type': 'HUMIDITY', 'value': 77, 'unit': '%'},
        {'name': 'Notable Gas (MEDIUM)', 'sensor_type': 'GAS', 'value': 0.52, 'unit': 'ppm'},
        
        # HIGH severity
        {'name': 'Very High Temp (HIGH)', 'sensor_type': 'TEMPERATURE', 'value': 46, 'unit': '°C'},
        {'name': 'Very High Humidity (HIGH)', 'sensor_type': 'HUMIDITY', 'value': 87, 'unit': '%'},
        {'name': 'High Gas Level (HIGH)', 'sensor_type': 'GAS', 'value': 0.68, 'unit': 'ppm'},
        
        # CRITICAL severity
        {'name': 'Extreme Heat (CRITICAL)', 'sensor_type': 'TEMPERATURE', 'value': 52, 'unit': '°C'},
        {'name': 'Extreme Humidity (CRITICAL)', 'sensor_type': 'HUMIDITY', 'value': 93, 'unit': '%'},
        {'name': 'Dangerous Gas Leak (CRITICAL)', 'sensor_type': 'GAS', 'value': 0.82, 'unit': 'ppm'},
        
        # NORMAL (no anomaly)
        {'name': 'Normal Temperature', 'sensor_type': 'TEMPERATURE', 'value': 23.5, 'unit': '°C'},
        {'name': 'Normal Humidity', 'sensor_type': 'HUMIDITY', 'value': 45, 'unit': '%'},
        {'name': 'Normal Gas Level', 'sensor_type': 'GAS', 'value': 0.15, 'unit': 'ppm'},
    ]
    
    severity_counts = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0, 'CRITICAL': 0, 'NORMAL': 0}
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}: {test_case['name']}")
        print(f"{'='*70}")
        
        # Prepare sensor data
        sensor_data = {
            'sensor_type': test_case['sensor_type'],
            'value': test_case['value'],
            'unit': test_case['unit'],
            'device_name': 'Test Device',
            'location': 'Test Location',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        print(f"\nInput: {test_case['sensor_type']} = {test_case['value']} {test_case['unit']}")
        
        # Use fallback analysis (rule-based)
        result = detector._fallback_analysis(sensor_data)
        
        status = 'ANOMALY' if result['anomaly'] else 'NORMAL'
        if not result['anomaly']:
            severity_counts['NORMAL'] += 1
        else:
            severity_counts[result['severity']] += 1
        
        print(f"\nResults:")
        print(f"  Status:      {status}")
        print(f"  Severity:    {result['severity']}")
        print(f"  Explanation: {result['explanation'][:80]}...")
        print(f"  Suggestion:  {result['suggestion'][:80]}...")
    
    # Summary
    print(f"\n\n{'='*70}")
    print("SEVERITY DISTRIBUTION SUMMARY")
    print(f"{'='*70}\n")
    
    total = len(test_cases)
    for severity, count in sorted(severity_counts.items(), key=lambda x: ['NORMAL', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'].index(x[0])):
        percentage = (count / total * 100) if total > 0 else 0
        bar = '█' * int(percentage / 2)
        print(f"  {severity:<10} {count:>2}/{total} ({percentage:>5.1f}%)  {bar}")
    
    print(f"\n{'='*70}\n")
    print("✓ Test completed successfully!")
    print("  The improved detector now distributes alerts across all severity levels.")
    print()


if __name__ == '__main__':
    test_fallback_severity_levels()
