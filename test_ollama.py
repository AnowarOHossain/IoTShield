from iotshield_backend.ollama_anomaly_detector import OllamaAnomalyDetector

model_name = "llama3.2:1b"
detector = OllamaAnomalyDetector()

test_data = {
    "sensor_type": "TEMPERATURE",
    "value": 23.5,
    "unit": "°C",
    "device_name": "Test Device",
    "location": "Lab",
    "timestamp": "2026-01-27T12:00:00Z"
}

print(f"Testing Ollama with model: {model_name}")
print(f"Test data: {test_data}")
result = detector.analyze(test_data)
print(f"\nResult:")
print(result)