"""
Ollama Model Test Script
This script helps verify Ollama llama3.2:1b model is running and accessible.
"""
from iotshield_backend.ollama_anomaly_detector import OllamaAnomalyDetector

def main():
    print("\n" + "="*60)
    print("OLLAMA MODEL TEST (llama3.2:1b)")
    print("="*60 + "\n")
    
    detector = OllamaAnomalyDetector()
    
    prompt_data = {
        'sensor_type': 'TEMPERATURE',
        'value': 30.0,
        'unit': '°C',
        'device_name': 'Test Device',
        'location': 'Lab',
        'timestamp': '2026-01-27T12:00:00Z'
    }
    
    print("Testing Ollama with llama3.2:1b model...")
    print(f"Model: {detector.model_name}")
    print(f"Endpoint: {detector.ollama_host}")
    result = detector.analyze(prompt_data)
    
    print("\nResult:")
    print(result)
    print("\nTest complete!\n")

if __name__ == '__main__':
    main()
