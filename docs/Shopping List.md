# IoTShield - Shopping List for RoboticsBD Store

**Store:** RoboticsBD  
**Location:** House#5, Road#3, Sector#7, Uttara, Dhaka, Bangladesh  
**Phone:** 01792 007 004  
**Email:** ask@roboticsbd.com  
**Website:** https://store.roboticsbd.com/

## Product Details & Links

### 1. **DHT22 Temperature & Humidity Sensor**
- **Price:** Estimated ~150-200 BDT
- **Specifications:**
  - Digital output
  - 3.3V compatible
  - Temperature & Humidity measurement
- **Search on store:** https://store.roboticsbd.com/sensors/81-temperature-humidity
- **Status:** Need to check in-store

### 2. **Flame Sensor Fire Detection Module** ✓ CONFIRMED
- **Part Number:** RBD-0149
- **Price:** BDT 48
- **Specifications:**
  - Output: 1 Channel (Digital)
  - Voltage: 3.3/5V
  - Detection angle: ~60 degrees
  - Sensitivity: Adjustable (potentiometer)
  - Detection range: 760-1100 nm (infrared)
- **Link:** https://store.roboticsbd.com/sensors/149-flame-sensor-fire-detection-module-robotics-bangladesh.html
- **Status:** In Stock (70 items available)

### 3. **PIR Motion Sensor**
- **Price:** Estimated ~100-150 BDT
- **Specifications:**
  - Digital output (HIGH when motion detected)
  - 5V operating voltage
  - Detection range: ~7 meters
- **Search on store:** https://store.roboticsbd.com/sensors/79-motion-sensor-robotics-bangladesh
- **Status:** Need to check in-store

### 4. **LDR Light Sensor Module** ✓ CONFIRMED
- **Part Number:** RBD-0823
- **Price:** BDT 75
- **Specifications:**
  - Output: Analog (ADC input)
  - Voltage: 5V
  - Light detection module with onboard resistor
- **Link:** https://store.roboticsbd.com/sensors/823-optical-sensitive-resistance-light-detection-photosensitive-ldr-sensor-module-robotics-bangladesh.html
- **Status:** In Stock

### 5. **10kΩ Resistor**
- **Price:** Estimated ~10 BDT per piece
- **Quantity Needed:** 3 pieces (~30 BDT total)
- **Purpose:** Pullup resistors for DHT22 & LDR
- **Search on store:** Electronics components section

### 6. **Breadboard (830 points)**
- **Price:** Estimated ~80-100 BDT
- **Specifications:**
  - 830 connection points
  - For circuit prototyping
  - Standard dimensions
- **Minimum required for our wiring:** 600-point breadboard (recommended). 830-point is comfortable.
- **Search on store:** [https://store.roboticsbd.com/ (Search: breadboard)](https://store.roboticsbd.com/components/133-breadboard-full-size-bare-830-tie-points-robotics-bangladesh.html)
- **Status:** Need to check in-store

### 7. **Jumper Wires (Male-to-Male + Male-to-Female)**
- **Part Number:** RBD-0031 (M-M), RBD-? (M-F)
- **Price:** BDT 100 (M-M), ~BDT 100 (M-F)
- **Specifications:**
  - 20cm length
  - 40 pieces per pack (or 20-piece packs)
- **Exact jumper wire counts (based on 5 sensors):**
  - **Male-to-Male:** 15 pcs (3 wires × 5 sensors to breadboard)
  - **Male-to-Female:** 8 pcs (ESP32 → breadboard: 5 signal + 3 power lines)
- **Links:**
  - M-M: https://store.roboticsbd.com/robotics-parts/31-1-jumper-wire-40-pcs-set-20cm-robotics-bangladesh.html
  - M-F: https://store.roboticsbd.com/robotics-parts/31-1-jumper-wire-40-pcs-set-20cm-robotics-bangladesh.html
- **Note:** We need 40–50 pieces total. If only 20-piece packs are available, buy 2 packs.

---

## Complete Setup Instructions (ESP32-S3 + Sensors)

### 1) Prepare the ESP32-S3
1. Connect the ESP32-S3 to your PC using the USB-C cable.
2. Place the ESP32-S3 beside the breadboard (do not plug it into the breadboard).
3. Use **male-to-female** wires to connect ESP32 pins to the breadboard rails:
   - ESP32 **GND** → Breadboard GND rail
   - ESP32 **3.3V** → Breadboard 3.3V rail
   - ESP32 **5V** → Breadboard 5V rail

### 2) Breadboard Power Rails
1. Mark one rail as **3.3V**, one rail as **5V**, and one rail as **GND**.
2. Ensure all sensors share the same GND rail.

### 3) Connect Sensors (Using Male-to-Male Wires)

#### MQ2 Gas Sensor (Analog)
- **VCC** → 5V rail
- **GND** → GND rail
- **A0** → ESP32 GPIO **35** (ADC)

#### DHT22 Temperature & Humidity (Digital)
- **VCC** → 3.3V rail
- **GND** → GND rail
- **DATA** → ESP32 GPIO **32**
- Add **10kΩ resistor** between DATA and 3.3V (pull-up)

#### Flame Sensor (Analog)
- **VCC** → 5V rail
- **GND** → GND rail
- **A0** → ESP32 GPIO **36** (ADC)

#### PIR Motion Sensor (Digital)
- **VCC** → 5V rail
- **GND** → GND rail
- **OUT** → ESP32 GPIO **33**

#### LDR Light Sensor Module (Analog)
- **VCC** → 5V rail
- **GND** → GND rail
- **A0** → ESP32 GPIO **37** (ADC)

### 4) Final Check
1. Confirm all sensors share **GND**.
2. Confirm only **DHT22** uses **3.3V**; others use **5V**.
3. Confirm each sensor signal goes to a unique GPIO pin.
4. Plug in USB-C and upload firmware.

### 5) Quick Wiring Summary
- **ESP32 → Breadboard:** Use **male-to-female** wires.
- **Sensor → Breadboard:** Use **male-to-male** wires.

---

## Shopping Instructions

1. **Visit RoboticsBD Store:** Uttara, Dhaka (or order online)
2. **Confirmed Items:**
   - [ ] Flame Sensor (RBD-0149) - BDT 48
  - [ ] Jumper Wires (Male-to-Male, RBD-0031) - BDT 100
  - [ ] Jumper Wires (Male-to-Female) - ~BDT 100
   - [ ] LDR Sensor Module (RBD-0823) - BDT 75

3. **Items to Search for:**
   - [ ] DHT22 Temperature & Humidity Sensor
   - [ ] PIR Motion Sensor
   - [ ] Breadboard (830 points)
   - [ ] 10kΩ Resistor (3 pieces)
  - [ ] Jumper Wires (Male-to-Female)

4. **Call/Visit for availability:** 01792 007 004

---

## Alternatives Available at RoboticsBD

If specific items not available:
- **Temperature Sensor:** DS18B20 (BDT 150)
- **Motion Sensor:** RCWL-0516 Microwave Radar (BDT 144)
- **Breadboard:** Various sizes available
- **Gas Sensors:** MQ-7 (BDT 178), MQ-4, MQ-135, etc.

---

## Total Budget Estimate
- **Minimum:** ~600 BDT (with confirmed prices)
- **Maximum:** ~800 BDT (with estimates)
- **Currency:** Bangladeshi Taka (BDT)

---



*Last Updated: February 16, 2026*
*Store:** https://store.roboticsbd.com/
*Phone:** 01792 007 004
