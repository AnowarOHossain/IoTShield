# IoTShield - Getting Started Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` file with your settings:
- Set `GEMINI_API_KEY` for AI-powered alerts
- Configure MQTT broker settings
- Adjust privacy parameters

### 3. Setup Database

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Train ML Model

```bash
cd ml_models
python train_model.py
cd ..
```

### 5. Start MQTT Broker

Install Mosquitto:
- **Windows**: Download from https://mosquitto.org/download/
- **Ubuntu**: `sudo apt-get install mosquitto`
- **macOS**: `brew install mosquitto`

Start broker:
```bash
mosquitto -v -p 1883
```

### 6. Run Django Server

```bash
python manage.py runserver
```

Access dashboard at: http://localhost:8000

### 7. Start Simulator

In a new terminal:
```bash
cd simulator
python simulator.py
```

## 📊 System Components

1. **Django Backend** - Main application server
2. **MQTT Broker** - Message queue for IoT communication
3. **Simulator** - Generates sensor data
4. **Dashboard** - Web interface for monitoring
5. **ML Engine** - Anomaly detection

## 🔧 Troubleshooting

### MQTT Connection Issues
- Ensure Mosquitto is running
- Check firewall settings
- Verify broker host/port in config

### Gemini API Errors
- Verify API key in `.env`
- Check API quota limits
- System works without Gemini (fallback alerts)

### Database Errors
- Run migrations: `python manage.py migrate`
- Delete `db.sqlite3` and recreate

## 📚 Next Steps

- Configure real ESP32 devices
- Setup Raspberry Pi edge gateway
- Deploy to production server
- Configure SSL/TLS for MQTT
- Setup automated backups

## 🆘 Support

For issues, contact: anowarhossain.dev@gmail.com
