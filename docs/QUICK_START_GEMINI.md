# Quick Start: Testing the New Gemini Anomaly Detector

## Prerequisites
- Gemini API key configured in `.env` file
- Django environment activated

## Test Commands

### 1. Quick Test with Predefined Data
```bash
python manage.py test_gemini_detector --sensor-type TEMPERATURE --value 45.5
```

Expected output:
- Anomaly: True
- Severity: CRITICAL
- Explanation: Why temperature is anomalous
- Suggestion: What to do

### 2. Test with Different Sensor Types

```bash
# Test normal temperature
python manage.py test_gemini_detector --sensor-type TEMPERATURE --value 22.5

# Test high humidity
python manage.py test_gemini_detector --sensor-type HUMIDITY --value 85

# Test gas leak
python manage.py test_gemini_detector --sensor-type GAS --value 0.75
```

### 3. Comprehensive Testing

```bash
# Run all test cases
python test_gemini_anomaly.py --mode test

# Test with recent database records
python test_gemini_anomaly.py --mode recent

# Run both
python test_gemini_anomaly.py --mode both
```

### 4. Live System Test

```bash
# Terminal 1: Start Django server
python manage.py runserver

# Terminal 2: Start MQTT listener with new Gemini detector
python manage.py mqtt_listener

# Terminal 3: Start simulator
python simulator/simulator.py

# Terminal 4: Monitor alerts
python check_data.py
```

## What to Expect

### Normal Reading Example:
```
Input: Temperature = 22.5°C
Output:
  Anomaly: NO
  Severity: LOW
  Explanation: Temperature within normal range
  Suggestion: Continue monitoring
```

### Anomaly Example:
```
Input: Temperature = 48.3°C
Output:
  Anomaly: YES
  Severity: CRITICAL
  Explanation: Critically high temperature, fire hazard
  Suggestion: Check for fire, inspect HVAC system
```

## Troubleshooting

### Issue: "Gemini API not configured"
**Solution**: Add GEMINI_API_KEY to your `.env` file

### Issue: "API timeout"
**Solution**: System will automatically use fallback detection

### Issue: "No response from Gemini"
**Solution**: Check internet connection, verify API key is valid

## Next Steps

1. Run tests to verify system works
2. Monitor logs for any errors
3. Check dashboard for new alerts
4. Review alert quality and accuracy

## Documentation

- System overview: `README.md`
- Code reference: `iotshield_backend/gemini_anomaly_detector.py`
- Other guides: `docs/` folder
