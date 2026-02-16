# Quick Start: Ollama + llama3.2:1b for IoTShield

## Get running in 5 minutes

## 1. Install Ollama (2 minutes)

```bash
# Windows/Mac
Visit https://ollama.ai and download installer

# Linux (Ubuntu/Debian)
curl https://ollama.ai/install.sh | sh
```

## 2. Pull Model (3 minutes)

```bash
ollama pull llama3.2:1b
```

Downloaded: ~2GB (first time only)

## 3. Start Ollama

```bash
ollama serve
```

Wait for:
```
time=2026-02-16 ... INFO server listen on 127.0.0.1:11434
```

## 4. Test in New Terminal

```bash
python test_ollama_models.py
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

## 5. Run IoTShield (As before)

```bash
# Terminal A: MQTT Broker
mosquitto

# Terminal B: Django Backend  
python manage.py runserver

# Terminal C: MQTT Listener
python manage.py mqtt_listener

# Terminal D: Dashboard
python manage.py runserver 0.0.0.0:8001
```

Visit: http://localhost:8001

---

## Configuration (.env)

Optional - if not set, defaults are used:

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b
```

---

## Troubleshooting

**Can't connect to Ollama?**
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# If fails, start Ollama
ollama serve
```

**Model not found?**
```bash
# Pull the model
ollama pull llama3.2:1b

# Verify
ollama list
```

**Slow inference?**
- Close other apps
- Check free RAM: `free -h`
- Reduce concurrent sensors

---

## What's Different?

| Before | After |
|--------|-------|
| TinyLlama + Transformers | Ollama + llama3.2:1b |
| 5-10s per analysis | 2-5s per analysis |
| 2.5GB VRAM needed | 1-2GB RAM needed |
| Complex PyTorch setup | Simple HTTP API |
| Lower accuracy | Better accuracy |

---

## Test Data Flow

```
Your PC (Ollama)
├─ http://localhost:11434  ← Ollama Service
├─ Port 1883              ← MQTT Broker
├─ Port 8000              ← Django Backend
└─ Port 8001              ← Dashboard
```

---

For detailed info: See `docs/OLLAMA_SETUP_GUIDE.md`
