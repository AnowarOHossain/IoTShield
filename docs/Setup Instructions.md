# IoTShield Hardware Setup Instructions
## Complete Guide for ESP32-S3 + Sensor Configuration

**Last Updated:** February 17, 2026  
**Status:** Ready for Hardware Assembly

---

## Table of Contents
1. [Components Checklist](#components-checklist)
2. [Hardware Setup](#hardware-setup)
3. [Wiring Diagram](#wiring-diagram)
4. [Step-by-Step Assembly](#step-by-step-assembly)
5. [Software Setup](#software-setup)
6. [Testing & Calibration](#testing--calibration)
7. [Troubleshooting](#troubleshooting)

---

## Components Checklist

### Main Microcontroller
- [x] ESP32-S3 Development Board
- [x] USB-C Cable (for power and programming)

### Sensors
- [x] MQ2 Gas Sensor (Analog)
- [x] DHT11 Temperature & Humidity Sensor (Digital)
- [x] Flame Sensor Fire Detection Module (Analog)
- [x] HC-SR501 PIR Motion Sensor (Digital)
- [x] LDR Photosensitive Resistor Sensor (Analog)

### Passive Components & Wiring
- [x] Breadboard (830 connection points)
- [x] Jumper Wires Male-to-Female (25 pieces)
- [x] Jumper Wires Male-to-Male (15 pieces)

### Optional Components
- [ ] 10kΩ Resistor (pull-up for DHT11, optional)
- [ ] USB Power Adapter (if not using PC for power)

---

## Hardware Setup

### Key Principles
1. **Do NOT plug ESP32-S3 directly into breadboard** - Use male-to-female wires instead
2. **All sensors share the same GND rail** - This is critical for proper operation
3. **Use correct voltage for each sensor** - MQ2, Flame, PIR, LDR need 5V; DHT11 works with 3.3V or 5V
4. **Keep wires organized** - Use different colored wires for power, ground, and signal
5. **Double-check connections before powering on** - Incorrect connections can damage sensors

---

## Wiring Diagram

```
                    +--------------------+
                    |   ESP32-S3         |
                    |   (beside board)   |
                    +--------------------+
                          |
          +--------+-------+-------+-------+
          |        |       |       |       |
        USB-C    5V      3.3V    GND    GPIO
         Cable   (out)   (out)   (out)   (in/out)


BREADBOARD LAYOUT:

┌─────────────────────────────────────────────────────┐
│ +5V Rail  │ +3.3V Rail │ GND Rail │  Signal Rails   │
├─────────────────────────────────────────────────────┤
│  MQ2-VCC  │  DHT11-VCC │ ALL GND  │ GPIO35 (MQ2)   │
│ Flame-VCC │            │          │ GPIO32 (DHT11) │
│  PIR-VCC  │            │          │ GPIO33 (PIR)   │
│  LDR-VCC  │            │          │ GPIO36 (Flame) │
│           │            │          │ GPIO37 (LDR)   │
└─────────────────────────────────────────────────────┘
```

---

## Step-by-Step Assembly

### Phase 1: Breadboard Preparation (5 minutes)

1. **Place breadboard on clean, stable surface**
   - Ensure good lighting for accurate wiring
   - Keep sensors nearby but organized

2. **Identify power rails**
   - Left rail: **5V** (for MQ2, Flame, PIR, LDR)
   - Middle rail: **3.3V** (for DHT11)
   - Right rail: **GND** (ground - for all sensors)
   - Rest: Signal channels

3. **Mark power rails with labels** (use tape or labels)
   - This prevents connection mistakes

### Phase 2: ESP32-S3 Connection (5 minutes)

1. **Connect ESP32-S3 to breadboard power:**
   - ESP32 **VIN (5V)** → Breadboard **5V rail** (use male-to-female wire)
   - ESP32 **3V3** → Breadboard **3.3V rail** (use male-to-female wire)
   - ESP32 **GND** → Breadboard **GND rail** (use male-to-female wire)

2. **Verify connections visually**
   - Ensure wires are fully inserted
   - Check for loose connections

### Phase 3: MQ2 Gas Sensor (5 minutes)

**Location:** Lower left of breadboard

| Pin | Connect To | Wire Type |
|-----|-----------|-----------|
| VCC | 5V rail | M-M (red) |
| GND | GND rail | M-M (black) |
| A0 | GPIO35 | M-M (yellow) |

**Steps:**
1. Insert MQ2 pins into breadboard
2. Connect VCC pin to 5V rail using red jumper wire
3. Connect GND pin to GND rail using black jumper wire
4. Connect A0 pin to GPIO35 signal rail using yellow jumper wire

### Phase 4: DHT11 Temperature & Humidity Sensor (5 minutes)

**Location:** Upper middle of breadboard

| Pin | Connect To | Wire Type |
|-----|-----------|-----------|
| VCC | 5V rail | M-M (red) |
| GND | GND rail | M-M (black) |
| DATA | GPIO32 | M-M (green) |

**Steps:**
1. Insert DHT11 pins into breadboard
   - Pin 1 = VCC
   - Pin 2 = DATA
   - Pin 3 = NC (not connected)
   - Pin 4 = GND
2. Connect VCC to 5V rail (DHT11 is 3.3-5V compatible)
3. Connect GND to GND rail
4. Connect DATA to GPIO32 signal rail
5. (Optional) Add 10kΩ pull-up resistor between DATA and VCC if signal is unreliable

### Phase 5: Flame Sensor (5 minutes)

**Location:** Lower middle of breadboard

| Pin | Connect To | Wire Type |
|-----|-----------|-----------|
| VCC | 5V rail | M-M (red) |
| GND | GND rail | M-M (black) |
| A0 | GPIO36 | M-M (orange) |

**Steps:**
1. Insert Flame sensor pins into breadboard
2. Connect VCC to 5V rail
3. Connect GND to GND rail
4. Connect A0 to GPIO36 signal rail

### Phase 6: PIR Motion Sensor (5 minutes)

**Location:** Upper right of breadboard

| Pin | Connect To | Wire Type |
|-----|-----------|-----------|
| VCC | 5V rail | M-M (red) |
| GND | GND rail | M-M (black) |
| OUT | GPIO33 | M-M (purple) |

**Steps:**
1. Insert PIR sensor pins into breadboard
2. Connect VCC to 5V rail
3. Connect GND to GND rail
4. Connect OUT to GPIO33 signal rail

**Important:** Allow 60 seconds for PIR sensor to calibrate after power-on

### Phase 7: LDR Light Sensor (5 minutes)

**Location:** Lower right of breadboard

| Pin | Connect To | Wire Type |
|-----|-----------|-----------|
| VCC | 5V rail | M-M (red) |
| GND | GND rail | M-M (black) |
| A0 | GPIO37 | M-M (blue) |

**Steps:**
1. Insert LDR sensor pins into breadboard
2. Connect VCC to 5V rail
3. Connect GND to GND rail
4. Connect A0 to GPIO37 signal rail

---

## Final Hardware Checklist

- [ ] All sensors connected to correct GPIO pins
- [ ] All sensors share same GND rail
- [ ] 5V sensors connected to 5V rail
- [ ] DHT11 connected to 5V rail
- [ ] No loose jumper wires
- [ ] No crossed or tangled wires
- [ ] All connections are tight
- [ ] USB cable connected to ESP32-S3
- [ ] Breadboard positioned for easy access

---

## Software Setup

### Step 1: Install Arduino IDE
1. Download from https://www.arduino.cc/en/software
2. Install on your PC
3. Launch Arduino IDE

### Step 2: Install ESP32 Board Support
1. Go to **File → Preferences**
2. Add this URL to "Additional Boards Manager URLs":
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Go to **Tools → Board → Boards Manager**
4. Search for "ESP32"
5. Install "ESP32 by Espressif Systems" (latest version)

### Step 3: Select ESP32-S3 Board
1. Go to **Tools → Board → ESP32 Arduino**
2. Select **"ESP32S3 Dev Module"**
3. Go to **Tools** and set:
   - Board: ESP32S3 Dev Module
   - Upload Speed: 921600
   - USB Mode: Hardware CDC and JTAG
   - Core Debug Level: None

### Step 4: Install Required Libraries
1. Go to **Sketch → Include Library → Manage Libraries**
2. Install the following:
   - `DHT sensor library` by Adafruit
   - `Adafruit Unified Sensor` by Adafruit
   - `ArduinoJson` by Benoit Blanchon
   - `PubSubClient` by Nick O'Leary (for MQTT)

### Step 5: Connect ESP32-S3
1. ConnectESP32-S3 to PC via USB-C cable
2. Go to **Tools → Port**
3. Select the COM port for ESP32-S3

### Step 6: Upload Firmware
1. Open or create your Arduino sketch for IoTShield
2. Configure WiFi credentials and MQTT broker address
3. Click **Upload** button
4. Wait for "Upload Complete" message

---

## Testing & Calibration

### Test 1: Serial Monitor Check
1. After upload, open **Tools → Serial Monitor**
2. Set baud rate to **115200**
3. Check for initialization messages
4. Verify each sensor appears in output

### Test 2: MQ2 Gas Sensor
- **Expected reading:** 300-400 (clean air)
- **With lighter (simulate gas):** 600+ (alarm range)
- Preheat: 20-30 seconds for stable reading

### Test 3: DHT11 Temperature & Humidity
- **Expected reading:** Room temperature (20-30°C) and humidity (30-70%)
- Check for "NA" or errors (may indicate pull-up resistor needed)

### Test 4: Flame Sensor
- **Expected reading:** 0 (no flame)
- **With lighter/flame:** 1 or high value
- Adjust sensitivity with potentiometer on sensor if needed

### Test 5: PIR Motion Sensor
- **Wait 60 seconds** after power-on (calibration period)
- **Expected reading:** 0 (no motion)
- **With motion in front:** 1 (motion detected)

### Test 6: LDR Light Sensor
- **Expected reading:** 0-1023 (dark) to 3000-4095 (bright light)
- Cover with hand: Value should increase
- Shine light: Value should decrease

### Calibration Steps
1. Run sensors for 5 minutes in normal environment
2. Note baseline readings for each sensor
3. Update threshold values in firmware if needed
4. Keep baseline values for anomaly detection algorithm

---

## Troubleshooting

### Issue: ESP32-S3 Not Recognized
**Solution:**
- Install CH340 USB driver from https://sparks.gogo.co.nz/ch340.html
- Try different USB cable (some are charge-only)
- Try different USB port (USB 3.0 ports sometimes have issues)

### Issue: Upload Fails
**Solution:**
- Hold BOOT button while uploading
- Change upload speed to 115200
- Restart Arduino IDE
- Reinstall ESP32 board package

### Issue: Serial Monitor Shows No Output
**Solution:**
- Check baud rate is 115200
- Disconnect and reconnect USB
- Check port selection in Tools menu
- Reset ESP32 (press RST button)

### Issue: MQ2 Sensor Not Responding
**Solution:**
- Check GPIO35 connection
- Ensure 5V is connected
- Wait for preheat (30 seconds)
- Check A0 pin is not pulled to GND accidentally

### Issue: DHT11 Sensor Reading "NA" or "-1"
**Solution:**
- Add 10kΩ pull-up resistor between DATA and VCC
- Check GPIO32 connection
- Ensure sensor VCC is connected to 5V (not 3.3V)
- Keep wires short (under 50cm)

### Issue: PIR Sensor Always Shows 1 (Motion)
**Solution:**
- Wait full 60 seconds for calibration after power-on
- Ensure sensor is not in direct sunlight
- Reduce sensitivity potentiometer on sensor
- Keep sensor away from heat sources

### Issue: LDR Sensor Shows Constant High Value
**Solution:**
- Check GPIO37 is connected
- Reduce light source if too bright
- Check for loose connections on A0 pin
- Verify breadboard contact points aren't damaged

### Issue: Inconsistent Sensor Readings
**Solution:**
- Check all GND connections are tight
- Verify breadboard contact points
- Reduce electromagnetic interference (away from WiFi router)
- Add small capacitors (0.1µF) across VCC-GND on sensor boards if available

---

## Safety Precautions

1. **Never power on without checking connections first**
2. **Do not touch sensor pins while powered**
3. **Disconnect USB before moving sensors**
4. **Do not expose MQ2 to direct flame** (use lighter for testing only)
5. **Keep water away from breadboard and electronics**
6. **Check for short circuits** before powering (use multimeter if available)
7. **Do not exceed 5V on any sensor pin**
8. **Ensure good ventilation** when testing gas sensors

---

## Next Steps

1. Complete hardware assembly as per instructions
2. Test each sensor individually
3. Upload firmware to ESP32-S3
4. Verify sensor readings in Serial Monitor
5. Connect to MQTT broker for IoTShield backend
6. Monitor sensor data on web dashboard

For questions or issues, refer to:
- Shopping List: `docs/Shopping List.md`
- Hardware Links: Store RoboticsBD - 01792 007 004

---

**Assembly Time:** ~25-30 minutes  
**Testing Time:** ~15 minutes  
**Total Setup Time:** ~45 minutes  

Good luck with your IoTShield hardware setup!
