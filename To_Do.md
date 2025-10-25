# 📋 IoTShield - To-Do List

## ⚠️ System Status (Oct 25, 2025)
- ✅ Django Server: http://127.0.0.1:8000/ (Working)
- ✅ Dashboard, Devices, Alerts pages (Working)
- ✅ Admin Panel: /admin/ (username: anowar)
- ✅ Database: All models migrated
- ✅ Gemini API: Configured
- ❌ MQTT Broker: NOT INSTALLED (Critical blocker)
- ❌ ML Model: Trained but broken (10.55% accuracy)

---

## 🔴 Critical Tasks

### 1. MQTT Broker Setup
- [ ] Install Mosquitto: https://mosquitto.org/download/
- [ ] Start service: `mosquitto -v` (Windows) or `sudo systemctl start mosquitto` (Linux)
- [ ] Test connection
- **Blocks**: MQTT listener, IoT simulator, real-time data

### 2. ML Model Retraining
- [ ] Fix `ml_models/train_model.py` feature extraction (match 6 features in `anomaly_detector.py`)
- [ ] Retrain model: `python ml_models/train_model.py`
- [ ] Test: `python ml_models/evaluate_model.py`
- **Issue**: Model flags all data as anomalies

### 3. MQTT Listener
- [ ] Run: `python manage.py mqtt_listener`
- **Depends on**: MQTT broker running

### 4. IoT Simulator
- [ ] Configure: `simulator/config.json`
- [ ] Run: `python simulator/simulator.py`
- **Depends on**: MQTT broker running

---

## 🟡 Important Tasks

### 5. Test Gemini API
- [ ] Test with real anomaly data
- [ ] Verify AI suggestions work

### 6. Security (Production)
- [ ] Change SECRET_KEY in settings.py
- [ ] Set DEBUG=False
- [ ] Remove API key from .env (use secrets manager)
- [ ] Enable MQTT TLS/SSL

### 7. Testing
- [ ] Test dashboard with real data
- [ ] Test anomaly detection accuracy
- [ ] Test alert generation
- [ ] Test control commands

---

## 🟢 Optional

### 8. Database (Production)
- [ ] Switch to PostgreSQL/MySQL
- [ ] Configure and migrate

### 9. Notifications
- [ ] Email alerts
- [ ] SMS alerts (Twilio)

### 10. Hardware Integration
- [ ] Setup ESP32 + sensors
- [ ] Flash code and connect

### 11. Production Deployment
- [ ] Setup server (AWS/Heroku)
- [ ] Configure Gunicorn + Nginx
- [ ] SSL certificates

---

## ✅ Completed
- [x] Django setup + migrations
- [x] Admin user created
- [x] Dashboard UI (Tailwind + Chart.js)
- [x] ML model trained (needs retraining)
- [x] Dataset created (10k samples)
- [x] Jupyter notebook
- [x] Fixed views.py import error
- [x] Created missing templates

---

## 🐛 Known Issues
1. **ML Model**: 10.55% accuracy - feature mismatch between training/detection
2. **MQTT**: Not installed - blocks all IoT features
3. **No Data**: Dashboard empty (MQTT not running)

---

## � Next Steps
1. Install Mosquitto MQTT broker
2. Fix ML model training
3. Start MQTT listener
4. Run IoT simulator
5. Test end-to-end flow

---

*Updated: Oct 25, 2025 | Repo: https://github.com/AnowarOHossain/IoTShield*
