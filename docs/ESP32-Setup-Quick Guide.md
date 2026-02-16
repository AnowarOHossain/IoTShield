
# ESP32 Setup Checklist for Demo 2

## Pre-Demo Preparation Checklist

### Day 1 (January 8 - TODAY)

#### Hardware Preparation
- [ ] Locate ESP32 DevKit board
- [ ] Find USB cable (Micro-USB or USB-C depending on ESP32 model)
- [ ] Test USB cable with computer (ensure it's a data cable, not just charging)
- [ ] Identify ESP32 built-in LED (usually GPIO2)

#### Software Installation
- [ ] Download and install Arduino IDE (https://www.arduino.cc/en/software)
- [ ] Add ESP32 board support to Arduino IDE
  - File → Preferences → Additional Board Manager URLs
  - Add: `https://dl.espressif.com/dl/package_esp32_index.json`
  - Tools → Board → Boards Manager → Install "ESP32"
- [ ] Install required libraries:
  - Sketch → Include Library → Manage Libraries
  - Install: `PubSubClient` by Nick O'Leary
  - Install: `ArduinoJson` by Benoit Blanchon

#### Network Configuration
- [ ] Find your PC's local IP address:
  - Open Command Prompt (CMD)
  - Type: `ipconfig`
  - Note down "IPv4 Address" (e.g., 192.168.1.100)
- [ ] Ensure PC and WiFi router on same network
- [ ] Check WiFi is 2.4GHz (ESP32 doesn't support 5GHz)
- [ ] Note down WiFi SSID (name) and Password

#### Firmware Configuration
- [ ] Open `iotshield_esp32.ino` in Arduino IDE
- [ ] Update WiFi credentials:
  ```cpp
  const char* WIFI_SSID = "YourWiFiName";
  const char* WIFI_PASSWORD = "YourWiFiPassword";
  ```
- [ ] Update MQTT broker IP:
  ```cpp
  const char* MQTT_BROKER = "192.168.1.XXX";  // Your PC's IP
  ```
- [ ] Save the file

#### First Upload Test
- [ ] Connect ESP32 to computer via USB
- [ ] In Arduino IDE:
  - Tools → Board → ESP32 Arduino → "ESP32 Dev Module"
  - Tools → Port → Select COM port (COM3, COM4, etc.)
  - Tools → Upload Speed → 115200
- [ ] Click Verify to compile
- [ ] Fix any compilation errors
- [ ] Click Upload to flash firmware
- [ ] Wait for "Done uploading" message

#### Connection Verification
- [ ] Open Serial Monitor (Tools → Serial Monitor)
- [ ] Set baud rate to 115200
- [ ] Press ESP32 reset button
- [ ] Check for:
  - WiFi connection message
  - IP address displayed
  - MQTT connection success
  - Sensor data publishing messages

#### Backend Verification
- [ ] Start Mosquitto MQTT broker
- [ ] Start Django server
- [ ] Start MQTT listener: `python manage.py mqtt_listener`
- [ ] Open dashboard: http://127.0.0.1:8000
- [ ] Check "Devices" page for ESP32_HARDWARE_001
- [ ] Verify real-time data appearing

---

### Day 2 (January 9)

#### Testing & Validation
- [ ] Test ESP32 auto-reconnect (unplug and replug USB)
- [ ] Monitor data flow for 30 minutes
- [ ] Check database for ESP32 entries
- [ ] Verify anomaly alerts are generated
- [ ] Test LED blinking patterns

#### Documentation
- [ ] Take photos of ESP32 hardware setup
- [ ] Screenshot of Serial Monitor output
- [ ] Screenshot of ESP32 data in dashboard
- [ ] Document any issues and solutions

---

### Day 3 (January 10)

#### Demo Rehearsal
- [ ] Full system startup sequence practice
- [ ] Time the ESP32 connection process
- [ ] Practice explaining the code
- [ ] Prepare backup (pre-uploaded firmware)
- [ ] Test on presentation laptop (if different)

#### Backup Plans
- [ ] Save successful Serial Monitor log
- [ ] Record video of ESP32 working
- [ ] Export dashboard screenshots showing ESP32 data
- [ ] Keep USB cable and ESP32 easily accessible

---

### Day 4 (January 11 - DEMO DAY)

#### Pre-Demo Setup (30 minutes before)
- [ ] Charge laptop fully
- [ ] Connect ESP32 and verify it's working
- [ ] Start all backend services
- [ ] Open all necessary windows:
  - Arduino IDE with code
  - Serial Monitor
  - Web browser with dashboard
  - MQTT client (mosquitto_sub) for demo
- [ ] Test internet connectivity
- [ ] Close unnecessary applications

#### During Demo
- [ ] Show physical ESP32 hardware first
- [ ] Explain the code structure
- [ ] Upload firmware (or show pre-uploaded)
- [ ] Show Serial Monitor → WiFi connection
- [ ] Show Serial Monitor → MQTT connection
- [ ] Show Serial Monitor → Data publishing
- [ ] Show Dashboard → Real-time ESP32 data
- [ ] Explain sensor expansion capability

---

## Common Issues & Quick Fixes

### ESP32 Won't Connect to WiFi
**Quick Fix:**
1. Double-check WiFi name (SSID) - case sensitive!
2. Verify password is correct
3. Ensure using 2.4GHz WiFi (not 5GHz)
4. Move ESP32 closer to router
5. Restart router if needed

### Arduino Can't Find ESP32
**Quick Fix:**
1. Install ESP32 drivers: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
2. Try different USB port
3. Try different USB cable (must be data cable)
4. Press and hold BOOT button while uploading

### MQTT Connection Fails
**Quick Fix:**
1. Check Mosquitto is running: `mosquitto -v`
2. Check firewall isn't blocking port 1883
3. Verify PC IP address hasn't changed
4. Test MQTT: `mosquitto_pub -h localhost -t test -m "hello"`

### No Data in Dashboard
**Quick Fix:**
1. Restart MQTT listener: `python manage.py mqtt_listener`
2. Check Django server is running
3. Verify ESP32 is publishing (Serial Monitor)
4. Clear browser cache and reload

---

## Required Materials for Demo 2

### Hardware
- ESP32 DevKit board
- USB cable (Micro-USB or USB-C)
- Laptop with Arduino IDE installed

### Software (Pre-installed)
- Arduino IDE with ESP32 support
- PubSubClient library
- ArduinoJson library
- Mosquitto MQTT broker
- Django server ready

### Documentation (Printed/Digital)
- ESP32 firmware code (with comments)
- Network architecture diagram
- System flow diagram
- Screenshots of working system

---

## Demo Script

### 1. Introduction (1 minute)
"Today we're demonstrating our IoTShield system with a physical ESP32 microcontroller. This shows the practical implementation of our thesis project."

### 2. Show Hardware (1 minute)
- Hold up ESP32 board
- Point out WiFi antenna
- Show USB connection
- Explain it's ready for sensors

### 3. Show Firmware Code (2 minutes)
- Open Arduino IDE
- Highlight key sections:
  - WiFi configuration
  - MQTT setup
  - Sensor reading functions
  - JSON data formatting

### 4. Live Upload (2 minutes)
- Connect ESP32
- Click Upload
- Show compilation progress
- Wait for "Done uploading"

### 5. Show Serial Monitor (2 minutes)
- Open Serial Monitor
- Show WiFi connection
- Show MQTT connection
- Show real-time data publishing

### 6. Show Dashboard (2 minutes)
- Open web browser
- Navigate to dashboard
- Show ESP32 device listed
- Show real-time charts updating
- Show alerts being generated

### 7. Explain Architecture (1 minute)
"The data flow is: ESP32 → WiFi → MQTT Broker → Django Backend → Database → Web Dashboard. This demonstrates end-to-end IoT communication."

### 8. Q&A Preparation
**Expected Questions:**
- Q: "Why not use sensors?"
- A: "We have sensors, but for Demo 2 we're focusing on hardware integration. The firmware is ready - we just plug in the sensors."

- Q: "Is this secure?"
- A: "Yes, we implement privacy-preserving mechanisms in the backend, and MQTT can be secured with TLS for production."

- Q: "Can this scale?"
- A: "Absolutely. The architecture supports multiple ESP32 devices. We've tested with simulators and now proving it with hardware."

---

## Success Criteria

- [ ] ESP32 successfully connects to WiFi
- [ ] ESP32 successfully connects to MQTT broker
- [ ] Data publishes every 5 seconds
- [ ] Data appears in Django dashboard
- [ ] LED blinks to show activity
- [ ] System runs for at least 5 minutes without issues
- [ ] Anomalies are detected by AI
- [ ] Email alerts triggered for critical events

---

Good luck with Demo 2!

*Last Updated: January 8, 2026*
