# IoTShield Simulators

## Overview

This folder contains IoT device simulators for testing the IoTShield system without physical hardware.

## Available Simulators

### 1. ESP32 Simulator (`simulator.py`)
Simulates an ESP32 microcontroller with basic environmental sensors.

**Device Details:**
- Device ID: `ESP32_SIM_001`
- Location: Living Room
- Sensors: Temperature, Humidity, Gas, Flame, Motion, Light

**Configuration:** `config.json`

### 2. Raspberry Pi Simulator (`rpi_simulator.py`)
Simulates a Raspberry Pi Edge Gateway with environmental sensors + system metrics.

**Device Details:**
- Device ID: `RPI_SIM_001`
- Location: Kitchen
- Sensors: Temperature, Humidity, Gas, Flame, Motion, Light
- System Metrics: CPU Temperature, Memory Usage, Disk Usage

**Configuration:** `rpi_config.json`

## Usage

### Run Single Simulator

**ESP32 Simulator:**
```bash
cd simulator
python simulator.py
```

**Raspberry Pi Simulator:**
```bash
cd simulator
python rpi_simulator.py
```

### Run Both Simulators Simultaneously

```bash
cd simulator
python run_all_simulators.py
```

This will start both ESP32 and Raspberry Pi simulators in separate processes.

## Configuration

Each simulator has its own JSON configuration file:

### ESP32 Configuration (`config.json`)
```json
{
  "device": {
    "device_id": "ESP32_SIM_001",
    "device_name": "Living Room Sensor Hub",
    "publish_interval": 5
  },
  "mqtt": {
    "broker_host": "localhost",
    "broker_port": 1883
  }
}
```

### Raspberry Pi Configuration (`rpi_config.json`)
```json
{
  "device": {
    "device_id": "RPI_SIM_001",
    "device_name": "Kitchen Edge Gateway",
    "publish_interval": 5
  },
  "mqtt": {
    "broker_host": "localhost",
    "broker_port": 1883
  }
}
```

## Features

### Common Features (Both Simulators)
- ✅ Privacy-preserving noise injection
- ✅ Configurable sensor parameters
- ✅ Anomaly injection for testing
- ✅ MQTT communication
- ✅ Timestamp with timezone support
- ✅ Structured logging

### Raspberry Pi Specific Features
- ✅ System monitoring (CPU, Memory, Disk)
- ✅ Edge gateway simulation
- ✅ Extended sensor suite

## Data Flow

```
Simulator → MQTT Broker → Django Backend → Database → Dashboard
```

## Sensor Data Format

```json
{
  "device_id": "ESP32_SIM_001",
  "device_name": "Living Room Sensor Hub",
  "device_type": "SIMULATOR",
  "sensor_type": "TEMPERATURE",
  "value": 25.3,
  "unit": "°C",
  "location": "Living Room",
  "timestamp": "2025-11-06T10:30:45.123456+00:00"
}
```

## Requirements

- Python 3.10+
- paho-mqtt 2.1.0
- Active MQTT broker (Mosquitto)
- Django backend running

## Troubleshooting

**Issue: Connection refused**
- Ensure Mosquitto MQTT broker is running
- Check broker host/port in config files

**Issue: No data appearing in dashboard**
- Verify Django MQTT listener is running: `python manage.py mqtt_listener`
- Check MQTT topic matches in config

**Issue: Import errors**
- Ensure you're in the simulator directory when running
- Activate virtual environment first

## Testing

To verify simulators are working:

1. Start MQTT broker
2. Start Django server
3. Start MQTT listener
4. Run simulator(s)
5. Check dashboard at http://localhost:8000

You should see:
- Device count increasing
- Sensor readings appearing
- Real-time data updates
- Alerts for anomalies

## Customization

### Modify Sensor Ranges

Edit the `sensors` section in config files:

```json
"temperature": {
  "base_value": 25,
  "variance": 3,
  "anomaly_chance": 0.05
}
```

### Change Publish Interval

```json
"device": {
  "publish_interval": 10  // seconds
}
```

### Add New Sensor Type

1. Add sensor config to `config.json`
2. Create sensor reading method in `utils/sensors.py`
3. Add to sensor list in simulator code

## Files

- `simulator.py` - ESP32 simulator
- `rpi_simulator.py` - Raspberry Pi simulator
- `run_all_simulators.py` - Multi-device launcher
- `config.json` - ESP32 configuration
- `rpi_config.json` - Raspberry Pi configuration
- `utils/` - Shared utility modules
  - `sensors.py` - Sensor simulation logic
  - `mqtt_publisher.py` - MQTT client wrapper
  - `logger.py` - Logging setup

## Support

For issues or questions, contact: anowarhossain.dev@gmail.com
