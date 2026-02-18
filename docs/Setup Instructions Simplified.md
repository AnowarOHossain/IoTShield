# IoTShield Fast Setup - ESP32 + DHT11

**Super quick, breadboard method (ESP32 and DHT11 both plugged in).**

---

## What You Need

- ESP32 Dev Board
- DHT11 Sensor (4-pin)
- Breadboard
- 3 Jumper Wires
- USB Cable
- Arduino IDE

---

## 1) Plug into Breadboard

1. Insert the ESP32 into the breadboard (center gap).
2. Insert the DHT11 into the breadboard.

---

## 2) Connect Only 3 Wires

Use any GPIO you want (GPIO32 is common). This is the minimum working setup:

- DHT11 **VCC** → ESP32 **3V3**
- DHT11 **GND** → ESP32 **GND**
- DHT11 **DATA** → ESP32 **GPIO32**

If your DHT11 is unstable, add a 10kΩ resistor between **DATA** and **3V3**.

---

## 3) Arduino IDE (One-Time Setup)

1. Install Arduino IDE: https://www.arduino.cc/en/software
2. Add ESP32 support:
    - **File → Preferences**
    - Add URL:
       ```
       https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
       ```
    - **Tools → Board → Boards Manager** → install **ESP32 by Espressif Systems**
3. Select board: **Tools → Board → ESP32 Arduino → ESP32 Dev Module**
4. Select port: **Tools → Port**
5. Install library: **Sketch → Include Library → Manage Libraries** → search **DHT** → install **DHT sensor library by Adafruit**

---

## 4) Upload Test Code

```cpp
#include "DHT.h"

#define DHTPIN 32
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
   Serial.begin(115200);
   delay(2000);
   dht.begin();
}

void loop() {
   float h = dht.readHumidity();
   float t = dht.readTemperature();

   if (isnan(h) || isnan(t)) {
      Serial.println("DHT11 read failed");
   } else {
      Serial.print("T: ");
      Serial.print(t);
      Serial.print(" C, H: ");
      Serial.print(h);
      Serial.println(" %");
   }

   delay(2000);
}
```

Click **Upload**.

---

## 5) Check Output

**Tools → Serial Monitor**, set **115200** baud. You should see temperature and humidity.

---

## If It Does Not Work

- Check that VCC is on **3V3**, not VIN/5V.
- Re-seat the ESP32 and DHT11 firmly.
- Add a **10kΩ** resistor between **DATA** and **3V3**.

That is all you need for tomorrow.
