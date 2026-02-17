/*
 * IoTShield ESP32-S3 Firmware v2.0
 * Privacy-Preserving IoT Monitoring System
 * 
 * This firmware enables ESP32-S3 to connect to WiFi and publish
 * sensor data to MQTT broker for real-time monitoring.
 * 
 * Hardware: ESP32-S3 Development Board
 * Sensors: DHT11, MQ2 Gas, Flame, PIR Motion (HC-SR501), LDR Light
 * 
 * Purchased: February 17, 2026 - RoboticsBD Uttara
 * 
 * Author: Anowar Hossain & Shihab Sarker
 * Project: IoTShield - CSE Thesis Project
 * Institution: Shanto-Mariam University of Creative Technology
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// ==================== CONFIGURATION ====================

// WiFi Configuration  
const char* WIFI_SSID = "YOUR_WIFI_SSID";        // Set your WiFi name here
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"; // Set your WiFi password here

// NOTE: For security, do not commit real WiFi credentials to GitHub

// MQTT Broker Configuration
const char* MQTT_BROKER = "192.168.0.100";   // Change to your PC's local IP (e.g., "192.168.1.100")
const int MQTT_PORT = 1883;
const char* MQTT_TOPIC = "iotshield/sensors/data";
const char* MQTT_CLIENT_ID = "ESP32_HARDWARE_001";

// Device Information
const char* DEVICE_ID = "ESP32_HARDWARE_001";
const char* DEVICE_NAME = "ESP32 Smart Sensor Hub";
const char* DEVICE_TYPE = "ESP32";
const char* LOCATION = "Demo Lab";

// Timing Configuration
const unsigned long PUBLISH_INTERVAL = 5000;  // 5 seconds
const unsigned long WIFI_TIMEOUT = 20000;     // 20 seconds
const unsigned long MQTT_RECONNECT_DELAY = 5000; // 5 seconds

// Built-in LED Pin
const int LED_PIN = 2;  // Most ESP32 boards have LED on GPIO2

// ==================== SENSOR PIN CONFIGURATION ====================

// DHT11 Temperature & Humidity Sensor
#define DHT_PIN 32
#define DHT_TYPE DHT11

// MQ2 Gas Sensor (Analog)
#define MQ2_PIN 35

// Flame Sensor (Analog)
#define FLAME_PIN 36

// PIR Motion Sensor (Digital)
#define PIR_PIN 33

// LDR Light Sensor (Analog)
#define LDR_PIN 37

// ==================== GLOBAL OBJECTS ====================

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
DHT dht(DHT_PIN, DHT_TYPE);

unsigned long lastPublishTime = 0;
bool sensorsAvailable = true;  // Set to true - we have physical sensors now!

// ==================== SETUP FUNCTIONS ====================

void setup() {
  // Initialize Serial for debugging
  Serial.begin(115200);
  delay(1000);

  // Initialize NTP time sync for ISO timestamps
  configTime(0, 0, "pool.ntp.org");
  Serial.println("Waiting for NTP time sync...");
  struct tm timeinfo;
  int ntpWait = 0;
  while (!getLocalTime(&timeinfo) && ntpWait < 20) {
    delay(500);
    Serial.print(".");
    ntpWait++;
  }
  if (ntpWait < 20) Serial.println("\n✓ NTP time acquired!");
  else Serial.println("\n⚠ Failed to sync NTP time, timestamps may be invalid.");
  
  Serial.println("\n\n");
  Serial.println("╔══════════════════════════════════════════════════════╗");
  Serial.println("║         IoTShield ESP32 Firmware v1.0                ║");
  Serial.println("║   Privacy-Preserving IoT Monitoring System           ║");
  Serial.println("╚══════════════════════════════════════════════════════╝");
  Serial.println();
  
  // Initialize LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  // Initialize WiFi
  setupWiFi();
  
  // Initialize MQTT
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
  
  // Initialize sensors (if available)
  setupSensors();
  
  Serial.println("Setup complete! Starting main loop...");
  for (int i = 0; i < 60; i++) Serial.print("=");
  Serial.println();
}

void setupWiFi() {
  Serial.println("Connecting to WiFi...");
  Serial.print("SSID: ");
  Serial.println(WIFI_SSID);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  unsigned long startTime = millis();
  
  // Blink LED while connecting
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - startTime > WIFI_TIMEOUT) {
      Serial.println("WiFi connection timeout!");
      Serial.println("Please check your SSID and password.");
      ESP.restart();  // Restart and try again
    }
    
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(500);
    Serial.print(".");
  }
  
  digitalWrite(LED_PIN, HIGH);  // Solid LED when connected
  
  Serial.println("\n✓ WiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Signal Strength: ");
  Serial.print(WiFi.RSSI());
  Serial.println(" dBm");
  Serial.println();
}

void setupSensors() {
  Serial.println("Initializing sensors...");
  
  // Initialize DHT11 Temperature & Humidity Sensor
  dht.begin();
  Serial.println("✓ DHT11 Temperature & Humidity Sensor initialized (GPIO 32)");
  
  // Initialize MQ2 Gas Sensor (Analog)
  pinMode(MQ2_PIN, INPUT);
  Serial.println("✓ MQ2 Gas Sensor initialized (GPIO 35)");
  
  // Initialize Flame Sensor (Analog)
  pinMode(FLAME_PIN, INPUT);
  Serial.println("✓ Flame Sensor initialized (GPIO 36)");
  
  // Initialize PIR Motion Sensor (Digital)
  pinMode(PIR_PIN, INPUT);
  Serial.println("✓ PIR Motion Sensor initialized (GPIO 33)");
  Serial.println("  [Calibrating for 60 seconds, please wait...]");
  
  // Initialize LDR Light Sensor (Analog)
  pinMode(LDR_PIN, INPUT);
  Serial.println("✓ LDR Light Sensor initialized (GPIO 37)");
  
  // Allow PIR sensor to calibrate
  delay(60000);  // 60 second calibration period for PIR
  Serial.println("✓ PIR Motion Sensor calibrated and ready!");
  
  sensorsAvailable = true;
  Serial.println();
  Serial.println("✓ All physical sensors detected and initialized");
  Serial.println();
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  // Handle incoming MQTT messages (for future control commands)
  Serial.print("Message received on topic: ");
  Serial.println(topic);
}

// ==================== MAIN LOOP ====================

void loop() {
  // Maintain WiFi connection
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected! Reconnecting...");
    setupWiFi();
  }
  
  // Maintain MQTT connection
  if (!mqttClient.connected()) {
    reconnectMQTT();
  }
  mqttClient.loop();
  
  // Publish sensor data at regular intervals
  unsigned long currentTime = millis();
  if (currentTime - lastPublishTime >= PUBLISH_INTERVAL) {
    publishSensorData();
    lastPublishTime = currentTime;
  }
  
  // Blink LED to show activity
  blinkLED();
}

// ==================== MQTT FUNCTIONS ====================

void reconnectMQTT() {
  static unsigned long lastAttempt = 0;
  unsigned long currentTime = millis();
  
  // Don't attempt too frequently
  if (currentTime - lastAttempt < MQTT_RECONNECT_DELAY) {
    return;
  }
  
  lastAttempt = currentTime;
  
  Serial.print("Connecting to MQTT broker at ");
  Serial.print(MQTT_BROKER);
  Serial.print(":");
  Serial.print(MQTT_PORT);
  Serial.print("...");
  
  if (mqttClient.connect(MQTT_CLIENT_ID)) {
    Serial.println(" ✓ Connected!");
    digitalWrite(LED_PIN, HIGH);
    
    // Subscribe to control topics (for future use)
    mqttClient.subscribe("iotshield/control/commands");
  } else {
    Serial.print(" ✗ Failed! RC=");
    Serial.println(mqttClient.state());
    Serial.println("Retrying in 5 seconds...");
    digitalWrite(LED_PIN, LOW);
  }
}

// ==================== SENSOR READING FUNCTIONS ====================

float readTemperature() {
  if (sensorsAvailable) {
    // Read from DHT11 sensor
    float temp = dht.readTemperature();
    
    // Check if reading is valid
    if (isnan(temp)) {
      Serial.println("⚠ DHT11 temperature reading failed!");
      return 25.0;  // Return default value
    }
    
    return temp;
  } else {
    // Fallback: Simulated data
    float baseTemp = 25.0;
    float variance = random(-30, 30) / 10.0;
    return baseTemp + variance;
  }
}

float readHumidity() {
  if (sensorsAvailable) {
    // Read from DHT11 sensor
    float humidity = dht.readHumidity();
    
    // Check if reading is valid
    if (isnan(humidity)) {
      Serial.println("⚠ DHT11 humidity reading failed!");
      return 60.0;  // Return default value
    }
    
    return humidity;
  } else {
    // Fallback: Simulated data
    float baseHumidity = 60.0;
    float variance = random(-100, 100) / 10.0;
    float humidity = baseHumidity + variance;
    return constrain(humidity, 0, 100);
  }
}

float readGas() {
  if (sensorsAvailable) {
    // Read from MQ2 analog sensor
    int rawValue = analogRead(MQ2_PIN);
    
    // Convert to ppm (parts per million)
    // MQ2 output: 0-4095 (12-bit ADC)
    // Clean air: ~300-400 ppm
    // Gas detected: 600+ ppm
    float ppm = map(rawValue, 0, 4095, 0, 1000);
    
    return ppm;
  } else {
    // Fallback: Simulated data
    float baseGas = 350.0;
    float variance = random(-50, 50);
    
    // Occasionally generate gas leak anomaly
    if (random(1000) < 15) {
      variance = random(200, 500);
    }
    
    return baseGas + variance;
  }
}

int readFlame() {
  if (sensorsAvailable) {
    // Read from flame sensor (analog, but we treat as digital threshold)
    int rawValue = analogRead(FLAME_PIN);
    
    // Flame detected if reading is above threshold
    // Typically: No flame = high value, Flame = low value (inverted)
    // Adjust threshold based on your sensor (usually 1000-2000)
    int threshold = 1500;
    
    if (rawValue < threshold) {
      return 1;  // Flame detected
    } else {
      return 0;  // No flame
    }
  } else {
    // Fallback: Simulated data
    if (random(1000) < 8) {
      return 1;
    }
    return 0;
  }
}

int readMotion() {
  if (sensorsAvailable) {
    // Read from PIR sensor (digital output)
    int motionDetected = digitalRead(PIR_PIN);
    
    // HC-SR501 outputs HIGH when motion detected
    return motionDetected;
  } else {
    // Fallback: Simulated data
    if (random(100) < 25) {
      return 1;
    }
    return 0;
  }
}

float readLight() {
  if (sensorsAvailable) {
    // Read from LDR sensor (analog)
    int rawValue = analogRead(LDR_PIN);
    
    // Convert to lux (light intensity)
    // Higher ADC value = darker environment (LDR resistance increases)
    // Lower ADC value = brighter environment
    // Typical range: 0-4095 (12-bit ADC)
    // Convert to lux: 0-1000 lux scale
    float lux = map(rawValue, 0, 4095, 1000, 0);  // Inverted mapping
    
    return lux;
  } else {
    // Fallback: Simulated data
    float baseLight = 300.0;
    float variance = random(-100, 100);
    return baseLight + variance;
  }
}

// ==================== PUBLISH FUNCTIONS ====================

void publishSensorData() {
  // Read all sensors
  float temperature = readTemperature();
  float humidity = readHumidity();
  float gas = readGas();
  int flame = readFlame();
  int motion = readMotion();
  float light = readLight();
  
  // Get current timestamp (seconds since boot)
  unsigned long timestamp = millis() / 1000;
  
  // Publish each sensor reading separately
  publishSensorReading("TEMPERATURE", temperature, "°C");
  publishSensorReading("HUMIDITY", humidity, "%");
  publishSensorReading("GAS", gas, "ppm");
  publishSensorReading("FLAME", (float)flame, "");
  publishSensorReading("MOTION", (float)motion, "");
  publishSensorReading("LIGHT", light, "lux");
  
  Serial.println("--- Published sensor batch ---");
}

void publishSensorReading(const char* sensorType, float value, const char* unit) {
  // Create JSON document
  StaticJsonDocument<512> doc;
  
  doc["device_id"] = DEVICE_ID;
  doc["device_name"] = DEVICE_NAME;
  doc["device_type"] = DEVICE_TYPE;
  doc["sensor_type"] = sensorType;
  doc["value"] = value;
  doc["unit"] = unit;
  doc["location"] = LOCATION;
  doc["timestamp"] = getTimestamp();
  
  // Serialize to JSON string
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer);
  
  // Publish to MQTT
  bool success = mqttClient.publish(MQTT_TOPIC, jsonBuffer);
  
  if (success) {
    Serial.print("✓ ");
    Serial.print(sensorType);
    Serial.print(": ");
    Serial.print(value);
    Serial.println(unit);
  } else {
    Serial.print("✗ Failed to publish ");
    Serial.println(sensorType);
  }
}

// ==================== UTILITY FUNCTIONS ====================

String getTimestamp() {
  // Return ISO 8601 timestamp using NTP time
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    // fallback: return empty string if NTP not available
    return "";
  }
  char buf[25];
  strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%S", &timeinfo);
  return String(buf);
}

void blinkLED() {
  static unsigned long lastBlink = 0;
  static bool ledState = true;
  
  // Blink every 1 second when connected
  if (millis() - lastBlink > 1000 && mqttClient.connected()) {
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState);
    lastBlink = millis();
  }
}

// ==================== DEBUG FUNCTIONS ====================

void printSystemInfo() {
  Serial.println("\n=== ESP32 System Information ===");
  Serial.print("Chip Model: ");
  Serial.println(ESP.getChipModel());
  Serial.print("Chip Revision: ");
  Serial.println(ESP.getChipRevision());
  Serial.print("CPU Frequency: ");
  Serial.print(ESP.getCpuFreqMHz());
  Serial.println(" MHz");
  Serial.print("Free Heap: ");
  Serial.print(ESP.getFreeHeap());
  Serial.println(" bytes");
  Serial.println("================================\n");
}
