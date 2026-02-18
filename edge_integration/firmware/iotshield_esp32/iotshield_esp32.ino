/*
 * IoTShield ESP32-S3 Firmware v3.0 (FINAL DEFENSE - PRODUCTION READY)
 * Fixed: Sensor Fallback Simulation + Enhanced Debugging
 * Author: Anowar Hossain & Shihab Sarker
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// ==================== CONFIGURATION ====================

const char* WIFI_SSID = "SMUCT";        
const char* WIFI_PASSWORD = "smuct#17"; 

const char* MQTT_BROKER = "172.172.9.119"; // PC IP
const int MQTT_PORT = 1883;
const char* MQTT_TOPIC = "iotshield/sensors/data";
const char* MQTT_CLIENT_ID = "ESP32_HARDWARE_001";

// Device Info
const char* DEVICE_ID = "ESP32_HARDWARE_001";
const char* DEVICE_NAME = "ESP32 Smart Sensor Hub";
const char* LOCATION = "Demo Lab";

// Timing
const unsigned long PUBLISH_INTERVAL = 2000; // 2 Seconds (Fast for demo)
const unsigned long WIFI_TIMEOUT = 20000;
const unsigned long DHT_TIMEOUT = 3000; // Timeout for DHT reading

// LED
const int LED_PIN = 2;

// ==================== SENSOR MODE ====================
// Set to true for SIMULATED DATA (fallback), false for REAL SENSORS
boolean USE_SIMULATOR = false; // Will auto-switch to true if real sensors fail
boolean SENSOR_FAILED = false; // Flag to track if real sensor failed 

// ==================== CORRECT SENSOR PINS ====================
// Updated to match the board wiring
#define DHT_PIN 4          // GPIO 4
#define DHT_TYPE DHT11
#define MQ2_PIN 5          // GPIO 5
#define FLAME_PIN 6        // GPIO 6
#define LDR_PIN 7          // GPIO 7
#define PIR_PIN 8          // GPIO 8

// ==================== SENSOR SIMULATION STRUCTURE ====================
struct SensorData {
  float temperature;
  float humidity;
  float gas_percent;
  int flame_status;
  int motion;
  float light_lux;
  boolean is_simulated;
};

SensorData currentSensorData;
unsigned long lastSimulatorUpdate = 0;
int simulatorPhase = 0; // For realistic simulation patterns

// ==================== OBJECTS & CLOCK ====================

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
DHT dht(DHT_PIN, DHT_TYPE);

unsigned long lastPublishTime = 0;

// SOFTWARE CLOCK (To fix the Time Problem)
int hour = 10, minute = 0, second = 0;
unsigned long lastTick = 0;

// ==================== SETUP ====================

void setup() {
  Serial.begin(115200);
  delay(2000); // Allow serial to stabilize

  Serial.println("\n\n========================================");
  Serial.println("     IoTShield ESP32 v3.0 STARTING");
  Serial.println("========================================");

  // 1. Initialize Pins
  Serial.println("[SETUP] Initializing GPIO pins...");
  pinMode(LED_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);
  
  // Set analog pins as inputs
  pinMode(MQ2_PIN, INPUT);
  pinMode(FLAME_PIN, INPUT);
  pinMode(LDR_PIN, INPUT);
  
  Serial.println("[SETUP] GPIO pins configured!");
  
  // 2. Initialize DHT11
  Serial.println("[SETUP] Initializing DHT11 sensor...");
  dht.begin();
  delay(1000);
  
  // Test DHT reading
  float testTemp = dht.readTemperature();
  if (isnan(testTemp)) {
    Serial.println("[ERROR] DHT11 not responding - will use SIMULATOR MODE");
    USE_SIMULATOR = true;
    SENSOR_FAILED = true;
  } else {
    Serial.print("[SUCCESS] DHT11 responding! Temp: ");
    Serial.println(testTemp);
  }

  // 3. WiFi
  Serial.println("[SETUP] Starting WiFi connection...");
  setupWiFi();

  // 4. MQTT
  Serial.println("[SETUP] Configuring MQTT client...");
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setKeepAlive(60);
  
  Serial.println("\n========================================");
  Serial.println("     SETUP COMPLETE - Ready to run");
  Serial.println("========================================\n");
}


// ==================== MAIN LOOP ====================

void loop() {
  // 1. WiFi Reconnect
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[WARN] WiFi disconnected, reconnecting...");
    setupWiFi();
  }

  // 2. MQTT Reconnect
  if (!mqttClient.connected()) {
    Serial.println("[WARN] MQTT disconnected, reconnecting...");
    reconnectMQTT();
  }
  mqttClient.loop();

  // 3. Update Software Clock (1 second tick)
  if (millis() - lastTick >= 1000) {
    second++;
    if (second >= 60) { second = 0; minute++; }
    if (minute >= 60) { minute = 0; hour++; }
    if (hour >= 24) hour = 0;
    lastTick = millis();
  }

  // 4. Publish Data (Every 2 seconds)
  if (millis() - lastPublishTime >= PUBLISH_INTERVAL) {
    readAndPublishSensorData();
    lastPublishTime = millis();
  }
}

// ==================== SENSOR READING & PUBLISHING ====================

void readAndPublishSensorData() {
  Serial.println("\n[DATA] ===== Reading Sensor Data =====");

  // Read sensors (real or simulated)
  if (USE_SIMULATOR) {
    readSimulatedSensors();
  } else {
    readRealSensors();
  }

  // Generate Time String "2026-02-18T10:00:00"
  char timeStr[30];
  sprintf(timeStr, "2026-02-18T%02d:%02d:%02d", hour, minute, second);

  // Publish all readings
  Serial.println("[DATA] Publishing to MQTT...");
  publishOne("TEMPERATURE", currentSensorData.temperature, "C", timeStr);
  publishOne("HUMIDITY", currentSensorData.humidity, "%", timeStr);
  publishOne("GAS", currentSensorData.gas_percent, "%", timeStr);
  publishOne("FLAME", (float)currentSensorData.flame_status, "bool", timeStr);
  publishOne("MOTION", (float)currentSensorData.motion, "bool", timeStr);
  publishOne("LIGHT", currentSensorData.light_lux, "lux", timeStr);

  // Status indicator
  if (currentSensorData.is_simulated) {
    Serial.println("[WARNING] Using SIMULATED DATA (Real sensors unavailable)");
  } else {
    Serial.println("[SUCCESS] All readings from REAL sensors");
  }
  Serial.println("[DATA] ===== End of Sensor Data =====\n");
  
  // Blink LED to show activity
  digitalWrite(LED_PIN, HIGH);
  delay(100);
  digitalWrite(LED_PIN, LOW);
}

// ==================== REAL SENSOR READING ====================

void readRealSensors() {
  Serial.println("[REAL] Reading real sensors...");
  
  // 1. Read DHT11
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("[ERROR] DHT11 read failed! Switching to SIMULATOR mode");
    USE_SIMULATOR = true;
    SENSOR_FAILED = true;
    readSimulatedSensors();
    return;
  }

  // 2. Read Analog Sensors
  int gasRaw = analogRead(MQ2_PIN);
  float gasPercent = (gasRaw / 4095.0) * 100.0;

  int flameRaw = digitalRead(FLAME_PIN);
  int flameStatus = (flameRaw == LOW) ? 1 : 0; // LOW = fire detected

  int motion = digitalRead(PIR_PIN);

  int lightRaw = analogRead(LDR_PIN);
  float lightLux = (1.0 - (lightRaw / 4095.0)) * 500.0;

  // Store in structure
  currentSensorData.temperature = temp;
  currentSensorData.humidity = hum;
  currentSensorData.gas_percent = gasPercent;
  currentSensorData.flame_status = flameStatus;
  currentSensorData.motion = motion;
  currentSensorData.light_lux = lightLux;
  currentSensorData.is_simulated = false;

  // Debug output
  Serial.print("[REAL] Temp: "); Serial.print(temp); Serial.println("°C");
  Serial.print("[REAL] Humidity: "); Serial.print(hum); Serial.println("%");
  Serial.print("[REAL] Gas: "); Serial.print(gasPercent); Serial.println("%");
  Serial.print("[REAL] Flame: "); Serial.println(flameStatus);
  Serial.print("[REAL] Motion: "); Serial.println(motion);
  Serial.print("[REAL] Light: "); Serial.print(lightLux); Serial.println(" lux");
}

// ==================== SIMULATED SENSOR READING ====================

void readSimulatedSensors() {
  Serial.println("[SIM] Generating simulated sensor data...");
  
  // Create realistic patterns for demo
  simulatorPhase = (simulatorPhase + 1) % 30;
  
  // Simulate temperature variation (23-28°C)
  currentSensorData.temperature = 25.0 + (2.0 * sin(simulatorPhase * 3.14159 / 15.0));
  
  // Simulate humidity (55-75%)
  currentSensorData.humidity = 65.0 + (10.0 * cos(simulatorPhase * 3.14159 / 15.0));
  
  // Simulate gas levels (5-30%)
  currentSensorData.gas_percent = 15.0 + (10.0 * sin(simulatorPhase * 3.14159 / 10.0));
  
  // Simulate intermittent flame (random)
  currentSensorData.flame_status = (random(100) < 20) ? 1 : 0;
  
  // Simulate motion (every 5 cycles)
  currentSensorData.motion = (simulatorPhase % 5 == 0) ? 1 : 0;
  
  // Simulate light variation (100-450 lux)
  currentSensorData.light_lux = 250.0 + (150.0 * cos(simulatorPhase * 3.14159 / 15.0));
  
  currentSensorData.is_simulated = true;

  // Debug output
  Serial.print("[SIM] Temp: "); Serial.print(currentSensorData.temperature); Serial.println("°C");
  Serial.print("[SIM] Humidity: "); Serial.print(currentSensorData.humidity); Serial.println("%");
  Serial.print("[SIM] Gas: "); Serial.print(currentSensorData.gas_percent); Serial.println("%");
  Serial.print("[SIM] Flame: "); Serial.println(currentSensorData.flame_status);
  Serial.print("[SIM] Motion: "); Serial.println(currentSensorData.motion);
  Serial.print("[SIM] Light: "); Serial.print(currentSensorData.light_lux); Serial.println(" lux");
}


void publishOne(const char* type, float value, const char* unit, const char* timeStr) {
  StaticJsonDocument<256> doc;
  doc["device_id"] = DEVICE_ID;
  doc["sensor_type"] = type;
  doc["value"] = value;
  doc["unit"] = unit;
  doc["timestamp"] = timeStr; // Dashboard displays this
  doc["location"] = LOCATION;
  doc["data_source"] = currentSensorData.is_simulated ? "SIMULATED" : "REAL";

  char buffer[256];
  serializeJson(doc, buffer);

  if (mqttClient.publish(MQTT_TOPIC, buffer)) {
    Serial.print("[MQTT] Published "); Serial.print(type); 
    Serial.print(" = "); Serial.print(value);
    Serial.print(" "); Serial.println(unit);
  } else {
    Serial.print("[MQTT ERROR] Failed to publish "); Serial.println(type);
  }
}


// ==================== CONNECTION HELPERS ====================

void setupWiFi() {
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("[WiFi] Already connected!");
    return;
  }
  
  Serial.print("[WiFi] Connecting to: ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WiFi] ✓ Connected!");
    Serial.print("[WiFi] IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[WiFi] ✗ Connection failed!");
  }
}

void reconnectMQTT() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[MQTT] WiFi not connected, cannot connect to MQTT");
    return;
  }
  
  Serial.print("[MQTT] Attempting connection...");
  String clientId = "ESP32-" + String(random(0xffff), HEX);
  
  if (mqttClient.connect(clientId.c_str())) {
    Serial.println(" ✓ Connected!");
    Serial.print("[MQTT] Client ID: ");
    Serial.println(clientId);
    Serial.print("[MQTT] Broker: ");
    Serial.print(MQTT_BROKER);
    Serial.print(":");
    Serial.println(MQTT_PORT);
  } else {
    Serial.print(" ✗ Failed (Code: ");
    Serial.print(mqttClient.state());
    Serial.println(")");
  }
}
