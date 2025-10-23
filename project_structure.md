# 🛡️ IoTShield – Project Structure

---

## 📚 Thesis Title
**Privacy-Preserving Real-Time Home Automation Utilizing MQTT Protocol and Sensor Anomaly Detection with GenAI Integration**

## 💡 Software System Name
**IoTShield**

### Tagline
*Smart Privacy-Preserving IoT Monitoring System — Powered by AI, Edge Computing, and Generative Intelligence*

---

## 📂 Root Directory Layout

```
IoTShield/
│
├── README.md
├── requirements.txt
├── project_structure.md
├── .env
├── manage.py
│
├── iotshield_backend/                # Django Backend Core
│   ├── __init__.py
│   ├── settings.py                   # Django settings (DB, MQTT, Gemini API keys)
│   ├── urls.py                       # Global URL routes
│   ├── asgi.py                       # For Django Channels (MQTT real-time)
│   ├── wsgi.py                       # For production (Gunicorn/Whitenoise)
│   ├── mqtt_client.py                # MQTT Subscriber (receives device data)
│   ├── gemini_alerts.py              # Gemini API alert generation logic
│   ├── anomaly_detector.py           # ML model: Isolation Forest / Autoencoder
│   ├── privacy_engine.py             # Privacy-preserving (noise & encryption)
│   ├── utils/
│   │   ├── db_helpers.py
│   │   ├── mqtt_utils.py
│   │   ├── logger.py
│   │   └── noise_utils.py
│   ├── models.py                     # Django ORM models (Devices, Sensors, Alerts)
│   ├── views.py                      # API endpoints
│   ├── serializers.py                # DRF serializers
│   └── routing.py                    # Django Channels WebSocket routing
│
├── dashboard/                        # Django App for Frontend Visualization
│   ├── __init__.py
│   ├── templates/
│   │   ├── dashboard.html            # Main IoT dashboard UI
│   │   ├── devices.html
│   │   ├── alerts.html
│   │   └── charts.html
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── views.py
│   ├── urls.py
│   └── charts.py                     # Real-time plotting via Plotly or Chart.js
│
├── simulator/                        # IoT Simulation Environment
│   ├── __init__.py
│   ├── simulator.py                  # Simulates ESP32 sensor data & publishes to MQTT
│   ├── actuator_sim.py               # Subscribes to actuation topic
│   ├── config.json                   # Broker URL, topics, device settings
│   ├── noise_generator.py            # Adds privacy-preserving Gaussian/Laplace noise
│   └── utils/
│       ├── sensors.py                # Generates fake temperature, humidity, motion, etc.
│       ├── mqtt_publisher.py         # Paho-MQTT publisher
│       └── logger.py
│
├── ml_models/                        # ML Model for anomaly detection
│   ├── __init__.py
│   ├── train_model.py                # Offline training script
│   ├── evaluate_model.py
│   ├── model.pkl                     # Trained model (e.g., IsolationForest)
│   ├── dataset/
│   │   └── sensor_data.csv
│   └── notebooks/
│       ├── anomaly_detection.ipynb
│       └── feature_engineering.ipynb
│
├── edge_integration/                 # Raspberry Pi / ESP32 integration
│   ├── esp32_client.py               # MicroPython-based MQTT publisher
│   ├── raspberry_pi_gateway.py       # Edge AI processing and forwarding
│   ├── device_config.json
│   └── firmware/
│       └── esp32_firmware.ino
│
├── docs/                             # Thesis Documentation and Research Files
│   ├── base_paper_summary.md
│   ├── literature_review.md
│   ├── system_design_diagram.png
│   ├── architecture_flowchart.png
│   ├── implementation_plan.md
│   └── thesis_report.docx
│
└── scripts/                          # Utility Scripts
    ├── run_mqtt_broker.sh
    ├── start_dashboard.sh
    ├── collect_data.py
    ├── generate_alerts.py
    └── backup_db.py
```

---

## ⚙️ Key Components Overview

| **Component** | **Description** |
|---------------|-----------------|
| `simulator/` | Python-based ESP32 simulator for sensor data with privacy noise. |
| `iotshield_backend/` | Core Django backend (MQTT listener, ML detection, Gemini alerts). |
| `ml_models/` | Machine Learning models for real-time anomaly detection. |
| `dashboard/` | Django app for front-end visualization & control dashboard. |
| `edge_integration/` | Scripts for physical ESP32/Raspberry Pi integration. |
| `docs/` | All thesis-related documentation and diagrams. |
| `scripts/` | Utility automation for running broker, dashboard, and data collection. |

---

## 🧩 MQTT Topic Structure

| **Topic** | **Description** |
|-----------|-----------------|
| `iotshield/sensors/data` | Raw (noisy) sensor data published from ESP32/simulator |
| `iotshield/anomalies` | ML-generated anomaly events |
| `iotshield/alerts` | Gemini-generated human-readable alerts |
| `iotshield/control/commands` | Commands to actuators |
| `iotshield/logs` | Internal system logs & events |

---

## 🚀 Data Flow (Simplified)

```
[ESP32 or Simulator] 
     ↓ (via MQTT)
[IoTShield Backend (Django + ML + Privacy)]
     ↓ (via Gemini API)
[Dashboard Alert Display]
     ↓
[Control Command]
     ↓ (via MQTT)
[Actuator or Raspberry Pi]
```

---

<div align="center">

### 🎯 **End-to-End Privacy-Preserving IoT Architecture**

</div>
