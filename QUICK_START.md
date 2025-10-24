# IoTShield - Quick Start Commands

## Windows Commands

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser (optional)
python manage.py createsuperuser

# 6. Train ML model
cd ml_models
python train_model.py
cd ..

# 7. Start Django server (Terminal 1)
python manage.py runserver

# 8. Start MQTT listener (Terminal 2 - after activating venv)
python manage.py mqtt_listener

# 9. Start simulator (Terminal 3 - after activating venv)
cd simulator
python simulator.py
```

## Note About MQTT Broker

Before running the system, make sure Mosquitto MQTT Broker is installed and running:

**Windows:**
- Download from: https://mosquitto.org/download/
- Install and start the service

**Check if running:**
```powershell
netstat -an | findstr "1883"
```

## Project Status

✅ Project structure created
✅ Core backend modules implemented
✅ Dashboard application ready
✅ IoT simulator configured
✅ ML model training script ready
✅ Documentation complete

## Next Steps After Setup

1. Install and start Mosquitto
2. Create virtual environment and install dependencies
3. Run migrations
4. Train ML model
5. Start all components
6. Access dashboard at http://localhost:8000

---

For detailed setup instructions, see SETUP_GUIDE.md
