# Ollama Setup Guide (llama3.2:1b) for IoTShield

This guide explains how to set up Ollama with the **llama3.2:1b** model for local, offline anomaly detection in IoTShield.

## Why Ollama + llama3.2:1b?

- **Local Processing**: No cloud API dependency (unlike Gemini)
- **Privacy**: All data stays on your machine
- **Cost Effective**: No API costs
- **Performance**: llama3.2:1b is optimized for 1.0B parameters - perfect for edge IoT devices
- **Fast Inference**: On i5 13th gen with 16GB RAM - ~2-5 seconds per analysis

## Prerequisites

- **Ollama Installed**: Download from [ollama.ai](https://ollama.ai)
- **Python Environment**: Your existing IoTShield Python environment
- **RAM**: Minimum 8GB RAM (16GB recommended for your setup)

## Installation Steps

### 1. Install Ollama

**Windows/Mac/Linux:**
```bash
# Download from https://ollama.ai
# Run the installer and follow the setup wizard
```

**Verify Installation:**
```bash
ollama --version
```

### 2. Pull the llama3.2:1b Model

```bash
ollama pull llama3.2:1b
```

This downloads the ~2GB model (first time only, takes a few minutes depending on internet speed).

**Verify Model is Available:**
```bash
ollama list
```

You should see `llama3.2:1b` in the list.

### 3. Start Ollama Server

**Terminal 1 - Start Ollama Service:**
```bash
ollama serve
```

You should see:
```
time=2026-02-16 time.Now() INFO server listen on 127.0.0.1:11434
```

The Ollama API runs on `http://localhost:11434` by default.

### 4. Configure IoTShield

#### Option A: Using Environment Variables (.env)

Create or update your `.env` file:

```env
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b
```

#### Option B: Using Django Settings

The settings are already configured in `iotshield_backend/settings.py`:
```python
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2:1b')
```

### 5. Test the Integration

**Test 1: Direct Ollama API Test**

```bash
# Terminal 2 (with Ollama running in Terminal 1)
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Is 45°C a normal room temperature?",
  "stream": false
}'
```

You should get a JSON response with the model's answer.

**Test 2: IoTShield Detector Test**

```bash
# Terminal 2 (with Ollama running)
python test_ollama_models.py
```

Or for comprehensive testing:
```bash
python test_ollama_anomaly.py --mode test
```

Expected output:
```
============================================================
OLLAMA MODEL TEST (llama3.2:1b)
============================================================

Testing Ollama with llama3.2:1b model...
Model: llama3.2:1b
Endpoint: http://localhost:11434

Test complete!
```

**Test 3: With Database Records**

```bash
python test_ollama_anomaly.py --mode recent
```

## Running IoTShield with Ollama

### Setup (One Time)

1. **Terminal 1 - Start MQTT Broker:**
```bash
./scripts/run_mqtt_broker.sh  # Or: mosquitto
```

2. **Terminal 2 - Start Ollama:**
```bash
ollama serve
```

3. **Terminal 3 - Start Django Backend:**
```bash
python manage.py runserver
```

4. **Terminal 4 - Start MQTT Listener:**
```bash
python manage.py mqtt_listener
```

5. **Terminal 5 - Start Dashboard:**
```bash
python manage.py runserver 0.0.0.0:8001
# Visit: http://localhost:8001
```

6. **Terminal 6 - Start Sensor Simulator (Optional):**
```bash
python simulator/run_all_simulators.py
```

## How It Works

```
Sensor Data → MQTT → Django Backend → Ollama (llama3.2:1b) → Alert → Dashboard
                                          ↓
                                    Local LLM Analysis
                                    (No Cloud API)
```

### Flow Example:

1. **Sensor sends:** `TEMPERATURE: 48°C` via MQTT
2. **Backend receives:** Stores in database, creates analysis prompt
3. **Ollama analyzes:** Sends prompt to `http://localhost:11434/api/generate`
4. **Model responds:** JSON with `{"anomaly": true, "severity": "HIGH", ...}`
5. **Alert created:** Database alert, MQTT broadcast, email notification
6. **Dashboard updates:** Real-time chart + alert display

## Troubleshooting

### Issue: "Cannot connect to Ollama at http://localhost:11434"

**Solution 1:** Verify Ollama is running
```bash
curl http://localhost:11434/api/tags
```

If it fails:
- Start Ollama: `ollama serve`
- Check firewall settings
- Verify port 11434 is open

**Solution 2:** Specify custom Ollama host
```bash
# In .env
OLLAMA_HOST=http://127.0.0.1:11434
```

### Issue: "Model llama3.2:1b not found"

**Solution:** Pull the model
```bash
ollama pull llama3.2:1b
```

Verify:
```bash
ollama list
```

### Issue: Slow inference (>15 seconds per analysis)

**Solution:**

1. **Check system resources:**
   ```bash
   # Linux/Mac
   free -h
   # Windows
   Get-Process ollama | Format-Table WS
   ```

2. **Reduce load:**
   - Close other applications
   - Reduce number of concurrent sensor readings
   - Use lighter model (not recommended): `phi:2.7b`

3. **Increase RAM allocation:**
   - Edit Ollama config
   - Add more system RAM

### Issue: "401 Unauthorized" or API errors

**Solution:** Check Ollama server logs
```bash
# Ollama will print errors in the terminal where you ran "ollama serve"
# Look for error messages
```

### Issue: JSON parsing errors in anomaly detector

**Solution:** Ensure Ollama is returning valid JSON
```bash
# Test manually
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "{\"test\": \"json\"}",
  "stream": false
}' | python -m json.tool
```

## Advanced Configuration

### Change Default Model

To use a different Ollama model (e.g., `qwen2.5:1.5b`):

1. **Pull the model:**
```bash
ollama pull qwen2.5:1.5b
```

2. **Update .env:**
```env
OLLAMA_MODEL=qwen2.5:1.5b
```

3. **Restart Django backend**

### Monitor Ollama Performance

Track request latency in logs:
```bash
# View IoTShield logs
tail -f logs/iotshield.log | grep "Ollama"
```

### API Parameters (Advanced)

Edit `iotshield_backend/ollama_anomaly_detector.py` to adjust:

```python
payload = {
    "model": self.model_name,
    "prompt": prompt,
    "stream": False,
    "temperature": 0.7,      # Lower = more deterministic
    "top_p": 0.9,           # Nucleus sampling parameter
    "top_k": 40             # Top-k sampling
}
```

## Comparison: TinyLlama vs Ollama (llama3.2:1b)

| Aspect | TinyLlama (Transformers) | Ollama (llama3.2:1b) |
|--------|--------------------------|----------------------|
| **Setup** | Manual model loading | Simple `ollama pull` |
| **Performance** | ~5-10s on CPU | ~2-5s on CPU |
| **Memory** | 2.5GB VRAM/RAM | 1-2GB RAM |
| **Code Complexity** | Medium (PyTorch) | Low (HTTP API) |
| **Model Quality** | Fair | Better (larger effective capacity) |
| **Maintenance** | More dependencies | Simpler |
| **Deployment** | Requires transformers, torch | Just needs Ollama running |

**Result:** Ollama + llama3.2:1b is cleaner, simpler, and better quality.

## Next Steps

1. ✅ Follow setup steps above
2. ✅ Test with provided test scripts
3. ✅ Run IoTShield with Ollama
4. ✅ Monitor logs for performance
5. ✅ Adjust parameters if needed (temperature, model)

## Documentation References

- [Ollama Official Docs](https://github.com/ollama/ollama)
- [Available Models](https://ollama.ai/library)
- [IoTShield Backend](../iotshield_backend/ollama_anomaly_detector.py)
- [MQTT Client Integration](../iotshield_backend/mqtt_client.py)

## Support

If you encounter issues:

1. Check Ollama server output for errors
2. Verify model is loaded: `ollama list`
3. Test API endpoint manually with curl
4. Check IoTShield logs: `logs/iotshield.log`
5. Ensure Django settings are correct: `iotshield_backend/settings.py`

---

**Last Updated:** February 16, 2026  
**IoTShield Version:** 2.1 (Ollama Integration)
