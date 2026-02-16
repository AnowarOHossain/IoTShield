"""
TinyLlama Model Test Script
This script helps verify TinyLlama model loading and basic inference.
"""
from iotshield_backend.tinylama_anomaly_detector import TinyLlamaAnomalyDetector

def main():
    print("\n" + "="*60)
    print("TINYLAMA MODEL TEST")
    print("="*60 + "\n")
    detector = TinyLlamaAnomalyDetector()
    prompt_data = {
        'sensor_type': 'TEMPERATURE',
        'value': 30.0,
        'unit': '°C',
        'device_name': 'Test Device',
        'location': 'Lab',
        'timestamp': '2026-01-27T12:00:00Z'
    }
    print("Testing TinyLlama model with sample data...")
    result = detector.analyze(prompt_data)
    print("\nResult:")
    print(result)
    print("\nTest complete!\n")

if __name__ == '__main__':
    main()
