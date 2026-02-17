# IoTShield - Shopping List for RoboticsBD Store

**Store:** RoboticsBD  
**Location:** House#5, Road#3, Sector#7, Uttara, Dhaka, Bangladesh  
**Phone:** 01792 007 004  
**Email:** ask@roboticsbd.com  
**Website:** https://store.roboticsbd.com/

## Product Details & Links

### 1. **DHT11 Temperature & Humidity Sensor** PURCHASED
- **Part Number:** RBD-0667
- **Price:** BDT 120
- **Specifications:**
  - Digital output
  - 3.3-5V compatible (more flexible than DHT22)
  - Temperature & Humidity measurement
  - Cheaper than DHT22 while maintaining good accuracy
- **Status:** Purchased on 17/02/2026

### 2. **Flame Sensor Fire Detection Module** CONFIRMED
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

### 3. **PIR Motion Sensor** PURCHASED
- **Part Number:** RBD-0023
- **Price:** BDT 93
- **Specifications:**
  - Digital output (HIGH when motion detected)
  - 5V operating voltage
  - Detection range: ~7 meters
  - Model: HC-SR501
- **Status:** Purchased on 17/02/2026

### 4. **LDR Light Sensor Module** PURCHASED
- **Part Number:** RBD-2093
- **Price:** BDT 50
- **Specifications:**
  - Output: Analog (ADC input)
  - Voltage: 5V
  - Light detection module with onboard resistor
- **Status:** Purchased on 17/02/2026

### 5. **10kΩ Resistor** (OPTIONAL - Not Purchased)
- **Price:** Estimated ~10 BDT per piece
- **Quantity Suggested:** 3 pieces (~30 BDT total)
- **Purpose:** Pull-up resistor for DHT11 (optional, for improved signal reliability)
- **Note:** DHT11 works without pull-up resistor on most boards, but recommended for long wire runs
- **Status:** Optional - Can be purchased later if needed

### 6. **Breadboard (830 points)** PURCHASED
- **Part Number:** RBD-0133
- **Price:** BDT 145
- **Specifications:**
  - 830 connection points
  - For circuit prototyping
  - Standard dimensions
- **Status:** Purchased on 17/02/2026

### 7. **Jumper Wires (Male-to-Male + Male-to-Female)** PURCHASED
- **Part Number:** RBD-1354 (both types)
- **Price:** BDT 45 (15x M-M) + BDT 75 (25x M-F) = BDT 120 total
- **Specifications:**
  - 20cm length
  - 15 pieces Male-to-Male
  - 25 pieces Male-to-Female
- **Status:** Purchased on 17/02/2026
- **Total provided:** 40 pieces (plenty for all sensors and future use)

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

#### DHT11 Temperature & Humidity (Digital)
- **VCC** → 3.3V/5V rail (DHT11 is 3.3-5V compatible)
- **GND** → GND rail
- **DATA** → ESP32 GPIO **32**
- Optional: Add **10kΩ resistor** between DATA and VCC (pull-up) for reliability

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

### PURCHASED TODAY (17/02/2026)
Order Ref: WYNFXCOAM | Order ID: 81374

**Items Purchased:**
- [x] Breadboard Full Size Bare 830 Tie Points - BDT 145
- [x] DHT11 Temperature & Humidity Sensor Module - BDT 120
- [x] Flame Sensor Fire Detection Module (RBD-0149) - BDT 48
- [x] HC-SR501 PIR Motion Sensor - BDT 93
- [x] Jumper Wires Male-to-Female (25 pcs) - BDT 75
- [x] Jumper Wires Male-to-Male (15 pcs) - BDT 45
- [x] LDR Photosensitive Resistor Sensor Module - BDT 50

**Total Cost:** BDT 576 (Paid via bKash)  
**Shipping:** Pickup from Store

### Original Shopping List (for Reference)
2. **Confirmed Items:**
   - [x] Flame Sensor (RBD-0149) - BDT 48
  - [x] Jumper Wires (Male-to-Male) - BDT 45
  - [x] Jumper Wires (Male-to-Female) - BDT 75
   - [x] LDR Sensor Module (RBD-0823) - BDT 50

3. **Items Obtained:**
   - [x] DHT11 Temperature & Humidity Sensor (instead of DHT22)
   - [x] PIR Motion Sensor (HC-SR501)
   - [x] Breadboard (830 points)

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
- **Actual Cost Paid:** **BDT 576** (17/02/2026)
- **Previous Budget Estimate:** ~600-800 BDT
- **Difference:** Saved BDT 24-224 due to better pricing on sensors
- **Currency:** Bangladeshi Taka (BDT)

### Cost Breakdown
- Breadboard: BDT 145
- Temperature Sensor (DHT11): BDT 120
- Humidity Sensor (DHT11): Included
- Flame Sensor: BDT 48
- PIR Motion Sensor: BDT 93
- LDR Light Sensor: BDT 50
- Jumper Wires (Combined): BDT 120 (25 M-F + 15 M-M)

---



*Last Updated: February 17, 2026 PURCHASED*
*Store:** https://store.roboticsbd.com/
*Phone:** 01792 007 004
*Payment Method:* bKash
*Pickup Status:* Completed from Uttara Store
