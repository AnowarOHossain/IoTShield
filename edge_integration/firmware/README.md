# IoTShield ESP32 Firmware

## Overview

Production-ready firmware for ESP32 microcontroller to integrate with IoTShield monitoring system. This firmware enables real-time sensor data collection and MQTT communication with the Django backend.

## Features

- WiFi connectivity with auto-reconnect
- MQTT client with persistent connection
- JSON data formatting compatible with Django backend
- Simulation mode (works without physical sensors)
- Status LED indicators
- Serial debugging output
- Modular sensor integration (DHT22, MQ2, Flame, PIR, LDR)
- Anomaly generation for demonstration
- Production-ready code structure

## Hardware Requirements

### Minimum (For Demo 2):
- **ESP32 DevKit** (any variant)
- **USB Cable** (for programming and power)
- **Computer** (for Arduino IDE)

### Complete System (Post Demo 2):
- ESP32 DevKit
- DHT22 Temperature & Humidity Sensor
- MQ2 Gas Sensor
- Flame Sensor Module
- PIR Motion Sensor
- LDR (Light Dependent Resistor)
- Jumper wires and breadboard

## Software Requirements

1. **Arduino IDE** (1.8.19 or later)
   - Download: https://www.arduino.cc/en/software

2. **ESP32 Board Support**
   - In Arduino IDE: File → Preferences
   - Add to "Additional Board Manager URLs":
     ```
     https://dl.espressif.com/dl/package_esp32_index.json
     ```
   - Tools → Board → Boards Manager → Search "ESP32" → Install

3. **Required Libraries** (Install via Library Manager):
   - `PubSubClient` by Nick O'Leary (v2.8 or later)
   - `ArduinoJson` by Benoit Blanchon (v6.21 or later)

## Quick Start Guide

### Step 1: Install Arduino IDE and Libraries

1. Download and install Arduino IDE
2. Add ESP32 board support (see above)
3. Install required libraries:
   - Sketch → Include Library → Manage Libraries
   - Search and install: `PubSubClient`, `ArduinoJson`

### Step 2: Configure the Firmware

Open `iotshield_esp32.ino` and update these settings:

```cpp
// WiFi Configuration
const char* WIFI_SSID = "YOUR_WIFI_SSID";        // Your WiFi name
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"; // Your WiFi password

// MQTT Broker Configuration
const char* MQTT_BROKER = "192.168.1.100";        // Your PC's local IP address
const int MQTT_PORT = 1883;
```

**Finding Your PC's IP Address:**
- Windows: Open CMD → Type `ipconfig` → Look for "IPv4 Address"
- Example: `192.168.1.100` or `192.168.0.101`

### Step 3: Upload to ESP32

1. Connect ESP32 to computer via USB
2. In Arduino IDE:
   - Tools → Board → ESP32 Arduino → "ESP32 Dev Module"
   - Tools → Port → Select your ESP32 port (COM3, COM4, etc.)
   - Tools → Upload Speed → 115200
3. Click "Upload" button
4. Wait for "Done uploading" message

### Step 3.5: Activate Mosquitto MQTT Broker

To enable MQTT communication, you need to start the Mosquitto broker on your PC:

1. Press **Win + R**, type `cmd`, and press Enter.
2. Navigate to the Mosquitto installation folder:
   ```
   cd "C:\Program Files\mosquitto"
   ```
3. Start the broker with the following command:
   ```
   mosquitto -c mosquitto.conf -v
   ```
4. Leave this window open while using the ESP32 and dashboard.

### Step 4: Monitor Serial Output

1. Tools → Serial Monitor
2. Set baud rate to: **115200**
3. You should see:
   ```
   ╔══════════════════════════════════════════════════════╗
   ║         IoTShield ESP32 Firmware v1.0                ║
   ║   Privacy-Preserving IoT Monitoring System           ║
   ╚══════════════════════════════════════════════════════╝
   
   Connecting to WiFi...
   WiFi Connected!
   IP Address: 192.168.1.150
   
   Connecting to MQTT broker... Connected!
   TEMPERATURE: 25.3°C
   HUMIDITY: 62.1%
   GAS: 0.08ppm
   ...
   ```

### Step 5: Verify Data in Django Dashboard

1. Ensure Mosquitto MQTT broker is running
2. Ensure Django server is running
3. Open dashboard: http://127.0.0.1:8000
4. Check "Devices" page → Should see "ESP32_HARDWARE_001"
5. Data should appear in real-time charts

## Configuration Options

### Device Settings

```cpp
const char* DEVICE_ID = "ESP32_HARDWARE_001";
const char* DEVICE_NAME = "ESP32 Smart Sensor Hub";
const char* DEVICE_TYPE = "ESP32";
const char* LOCATION = "Demo Lab";
```

### Timing Settings

```cpp
const unsigned long PUBLISH_INTERVAL = 5000;  // Publish every 5 seconds
const unsigned long WIFI_TIMEOUT = 20000;     // WiFi connection timeout
```

## Adding Physical Sensors (Post Demo 2)

### DHT22 Temperature & Humidity Sensor

1. **Wiring:**
   - VCC → 3.3V
   - GND → GND
   - DATA → GPIO4

2. **Code Changes:**
   ```cpp
   #include <DHT.h>
   
   #define DHT_PIN 4
   #define DHT_TYPE DHT22
   DHT dht(DHT_PIN, DHT_TYPE);
   
   void setupSensors() {
     dht.begin();
     sensorsAvailable = true;
   }
   
   float readTemperature() {
     if (sensorsAvailable) {
       return dht.readTemperature();
     }
     // ... simulation code ...
   }
   ```

### MQ2 Gas Sensor

1. **Wiring:**
   - VCC → 5V
   - GND → GND
   - AOUT → GPIO34

2. **Code:**
   ```cpp
   #define GAS_PIN 34
   
   float readGas() {
     if (sensorsAvailable) {
       int raw = analogRead(GAS_PIN);
       return raw / 4095.0;  // Convert to 0-1 range
     }
     // ... simulation code ...
   }
   ```

### PIR Motion Sensor

1. **Wiring:**
   - VCC → 5V
   - GND → GND
   - OUT → GPIO5

2. **Code:**
   ```cpp
   #define PIR_PIN 5
   
   int readMotion() {
     if (sensorsAvailable) {
       return digitalRead(PIR_PIN);
     }
     // ... simulation code ...
   }
   ```

## Data Format

The ESP32 publishes JSON messages to MQTT topic `iotshield/sensors/data`:

```json
{
  "device_id": "ESP32_HARDWARE_001",
  "device_name": "ESP32 Smart Sensor Hub",
  "device_type": "ESP32",
  "sensor_type": "TEMPERATURE",
  "value": 25.3,
  "unit": "°C",
  "location": "Demo Lab",
  "timestamp": "ESP32_TIME_12345"
}
```

## Troubleshooting

### Issue: WiFi Won't Connect
- Check SSID and password are correct
- Ensure WiFi is 2.4GHz (ESP32 doesn't support 5GHz)
- Check ESP32 is within WiFi range
- Try restarting ESP32 (press reset button)

### Issue: MQTT Connection Fails
- Ensure Mosquitto broker is running on your PC
- Check PC's firewall isn't blocking port 1883
- Verify MQTT_BROKER IP address is correct
- Ensure ESP32 and PC are on same WiFi network

### Issue: No Data in Dashboard
- Check Django server is running
- Check MQTT listener is running: `python manage.py mqtt_listener`
- Verify ESP32 is publishing (check Serial Monitor)
- Test MQTT with: `mosquitto_sub -h localhost -t "iotshield/sensors/data" -v`

### Issue: Upload Failed
- Select correct COM port
- Hold "BOOT" button during upload (some boards)
- Try different USB cable
- Reduce upload speed to 921600 or 460800

## Performance Metrics

- **Publish Rate**: Every 5 seconds (configurable)
- **WiFi Reconnection**: Automatic with 20s timeout
- **MQTT Reconnection**: Automatic with 5s retry delay
- **Memory Usage**: ~40KB RAM, ~200KB Flash
- **Power Consumption**: ~80mA active, ~10mA sleep (future)

## For Demo 2 Presentation

### Key Points to Highlight:

1. Real Hardware Integration - Physical ESP32 device
2. Production-Ready Code - Professional firmware structure
3. Wireless Communication - WiFi + MQTT protocol
4. Real-Time Data Flow - ESP32 → MQTT → Django → Dashboard
5. Scalable Architecture - Easy to add sensors later
6. Status Monitoring - LED indicators and serial debugging
7. Error Handling - Auto-reconnect for WiFi and MQTT

### Live Demo Flow:

1. Show ESP32 hardware
2. Upload firmware (if time permits)
3. Open Serial Monitor → Show connection logs
4. Show MQTT messages being published
5. Open Dashboard → Show real-time data from ESP32
6. Unplug ESP32 → Show reconnection
7. Explain sensor expansion plan

## Next Steps (Post Demo 2)

- [ ] Add DHT22 temperature/humidity sensor
- [ ] Add MQ2 gas sensor
- [ ] Add flame, motion, light sensors
- [ ] Implement OTA (Over-The-Air) updates
- [ ] Add deep sleep for power saving
- [ ] Implement NTP time synchronization
- [ ] Add local data buffering for offline operation
- [ ] Implement TLS/SSL for secure MQTT

## Additional Resources

- ESP32 Pinout: https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
- MQTT Protocol: https://mqtt.org/
- Arduino JSON: https://arduinojson.org/
- PubSubClient: https://pubsubclient.knolleary.net/

## Authors

- Anowar Hossain
- Shihab Sarker

**Supervisor**: Tahsin Alam, Lecturer  
**Institution**: Shanto-Mariam University of Creative Technology  
**Project**: IoTShield - Privacy-Preserving IoT Monitoring System

---

*Last Updated: January 8, 2026 | Demo 2: January 11, 2026*
