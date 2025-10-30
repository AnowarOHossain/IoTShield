# IoTShield - Complete Setup and Testing Guide

##  Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Mosquitto MQTT Broker
- Git (optional)

---

##  Complete Setup Instructions

### Step 1: Install Mosquitto MQTT Broker

#### Windows:
1. Download from: https://mosquitto.org/download/
2. Install and add to PATH
3. Start service: `net start mosquitto`

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

#### macOS:
```bash
brew install mosquitto
brew services start mosquitto
```

### Step 2: Setup Python Environment

```bash
# Navigate to project directory
cd IoTShield

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Edit the `.env` file:

```env
# Django Settings
SECRET_KEY=your-secret-key-change-this
DEBUG=True

# MQTT Configuration
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883

# Gemini API (Optional - for AI alerts)
GEMINI_API_KEY=your-gemini-api-key-here

# Privacy Settings
PRIVACY_NOISE_EPSILON=0.5
```

### Step 4: Initialize Database

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter username, email, and password when prompted
```

### Step 5: Train ML Model

```bash
cd ml_models
python train_model.py
cd ..
```

---

##  Running the System

### Terminal 1: Start MQTT Broker
```bash
# If not running as service
mosquitto -v -p 1883
```

### Terminal 2: Start Django Server
```bash
# Activate venv first
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Run server
python manage.py runserver
```

### Terminal 3: Start MQTT Listener
```bash
# Activate venv first
venv\Scripts\activate  # Windows

# Run MQTT listener
python manage.py mqtt_listener
```

### Terminal 4: Start IoT Simulator
```bash
# Activate venv first
venv\Scripts\activate  # Windows

# Run simulator
cd simulator
python simulator.py
```

---

##  Accessing the System

- **Dashboard**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Endpoints**: http://localhost:8000/api/

---

##  Testing the System

### 1. Verify MQTT Connection

```bash
# Subscribe to sensor data topic
mosquitto_sub -h localhost -t "iotshield/sensors/data" -v

# You should see sensor data being published
```

### 2. Check Dashboard

1. Open http://localhost:8000
2. You should see:
   - Active devices counter updating
   - Sensor readings appearing
   - Real-time charts updating
   - Alerts appearing when anomalies detected

### 3. Test API Endpoints

```bash
# Get sensor data
curl http://localhost:8000/api/sensors/data/

# Get alerts
curl http://localhost:8000/api/alerts/list/

# Get devices
curl http://localhost:8000/api/devices/list/

# Get statistics
curl http://localhost:8000/api/stats/summary/
```

### 4. Check Admin Panel

1. Go to http://localhost:8000/admin
2. Login with superuser credentials
3. Verify data:
   - Devices are being registered
   - Sensor data is being stored
   - Alerts are being generated

---

##  System Components Status Check

### Check if all components are running:

1.  **MQTT Broker**: `mosquitto_sub -h localhost -t "#" -v`
2.  **Django Server**: Visit http://localhost:8000
3.  **MQTT Listener**: Check terminal for connection message
4.  **Simulator**: Check terminal for publishing messages

---

##  Common Issues and Solutions

### Issue: MQTT Connection Failed

**Solution:**
- Check if Mosquitto is running: `ps aux | grep mosquitto` (Linux/Mac)
- Check port 1883 is not in use
- Verify firewall settings

### Issue: ModuleNotFoundError

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Database Errors

**Solution:**
```bash
# Delete database and recreate
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: No Sensor Data Appearing

**Solution:**
- Check if simulator is running
- Verify MQTT broker connection
- Check MQTT listener is running
- Review logs: `tail -f iotshield.log`

### Issue: Gemini API Errors

**Solution:**
- System works without Gemini API (uses fallback alerts)
- Get API key from: https://makersuite.google.com/app/apikey
- Add to `.env` file: `GEMINI_API_KEY=your-key-here`

---

##  Performance Tips

1. **For Production:**
   - Set `DEBUG=False` in settings
   - Use PostgreSQL instead of SQLite
   - Setup Nginx reverse proxy
   - Use Gunicorn for Django
   - Enable SSL/TLS for MQTT

2. **For Development:**
   - Keep DEBUG=True for detailed errors
   - Monitor logs regularly
   - Clear old sensor data periodically

---

##  Security Recommendations

1. Change SECRET_KEY in production
2. Use strong passwords for admin
3. Enable MQTT authentication
4. Use TLS/SSL for MQTT communication
5. Regularly update dependencies
6. Backup database regularly

---

##  Next Steps

1.  **Basic Setup Complete**
2. Configure real ESP32 devices
3. Setup Raspberry Pi gateway
4. Customize privacy parameters
5. Tune ML model for your environment
6. Add more sensor types
7. Deploy to cloud server

---

##  Support

- **Email**: anowarhossain.dev@gmail.com
- **GitHub Issues**: https://github.com/AnowarOHossain/IoTShield/issues
- **Documentation**: Check README.md and code comments

---

##  Success Indicators

Your system is working correctly when:

-  Dashboard shows active devices
-  Sensor data appears in real-time
-  Charts update automatically
-  Alerts appear for anomalous readings
-  Admin panel shows database entries
-  MQTT messages flowing (check with mosquitto_sub)

---

**Congratulations! Your IoTShield system is now operational! **
