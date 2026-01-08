/*
 * IoTShield ESP32 Firmware v1.0
 * Privacy-Preserving IoT Monitoring System
 * 
 * This firmware enables ESP32 to connect to WiFi and publish
 * sensor data to MQTT broker for real-time monitoring.
 * 
 * Hardware: ESP32 DevKit (or compatible)
 * Sensors: DHT22, MQ2, Flame, PIR Motion, LDR (Optional - can work without sensors)
 * 
 * Author: Anowar Hossain & Shihab Sarker
 * Project: IoTShield - CSE Thesis Project
 * Institution: Shanto-Mariam University of Creative Technology
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ==================== CONFIGURATION ====================

// WiFi Configuration (UPDATE THESE WITH YOUR NETWORK)
const char* WIFI_SSID = "YOUR_WIFI_SSID";        // Change this to your WiFi name
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"; // Change this to your WiFi password

// MQTT Broker Configuration
const char* MQTT_BROKER = "YOUR_PC_IP_ADDRESS";   // Change to your PC's local IP (e.g., "192.168.1.100")
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

// ==================== GLOBAL OBJECTS ====================

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

unsigned long lastPublishTime = 0;
bool sensorsAvailable = false;  // Set to true when physical sensors are connected

// ==================== SETUP FUNCTIONS ====================

void setup() {
  // Initialize Serial for debugging
  Serial.begin(115200);
  delay(1000);
  
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
  Serial.println("=".repeat(60));
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
  
  // TODO: Add sensor initialization code here when sensors are available
  // Example for DHT22:
  // dht.begin();
  
  // For Demo 2: Using simulated data (no physical sensors required)
  sensorsAvailable = false;
  
  if (sensorsAvailable) {
    Serial.println("✓ Physical sensors detected and initialized");
  } else {
    Serial.println("⚠ Running in simulation mode (no physical sensors)");
    Serial.println("  Generating realistic sensor data for demonstration");
  }
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
    // TODO: Read from DHT22 sensor
    // return dht.readTemperature();
    return 0.0;
  } else {
    // Simulated realistic temperature data
    float baseTemp = 25.0;
    float variance = random(-30, 30) / 10.0;  // ±3°C variance
    
    // Occasionally generate anomaly
    if (random(100) < 4) {  // 4% chance
      variance = random(-150, 150) / 10.0;  // Larger anomaly
    }
    
    return baseTemp + variance;
  }
}

float readHumidity() {
  if (sensorsAvailable) {
    // TODO: Read from DHT22 sensor
    // return dht.readHumidity();
    return 0.0;
  } else {
    // Simulated realistic humidity data
    float baseHumidity = 60.0;
    float variance = random(-100, 100) / 10.0;  // ±10% variance
    
    // Occasionally generate anomaly
    if (random(100) < 3) {  // 3% chance
      variance = random(-200, 200) / 10.0;  // Larger anomaly
    }
    
    float humidity = baseHumidity + variance;
    return constrain(humidity, 0, 100);  // Keep within 0-100%
  }
}

float readGas() {
  if (sensorsAvailable) {
    // TODO: Read from MQ2 sensor
    // return analogRead(GAS_PIN) / 4095.0;
    return 0.0;
  } else {
    // Simulated gas sensor (ppm)
    float baseGas = 0.08;
    float variance = random(-20, 20) / 1000.0;
    
    // Occasionally generate gas leak anomaly
    if (random(1000) < 15) {  // 1.5% chance
      variance = random(200, 500) / 1000.0;  // High gas reading
    }
    
    float gas = baseGas + variance;
    return constrain(gas, 0, 1.0);
  }
}

int readFlame() {
  if (sensorsAvailable) {
    // TODO: Read from flame sensor
    // return digitalRead(FLAME_PIN);
    return 0;
  } else {
    // Simulated flame sensor (0 = no flame, 1 = flame detected)
    if (random(1000) < 8) {  // 0.8% chance
      return 1;  // Flame detected
    }
    return 0;
  }
}

int readMotion() {
  if (sensorsAvailable) {
    // TODO: Read from PIR sensor
    // return digitalRead(PIR_PIN);
    return 0;
  } else {
    // Simulated motion sensor
    if (random(100) < 25) {  // 25% activity chance
      return random(1, 4);  // Motion intensity 1-3
    }
    return 0;
  }
}

float readLight() {
  if (sensorsAvailable) {
    // TODO: Read from LDR sensor
    // return analogRead(LDR_PIN);
    return 0.0;
  } else {
    // Simulated light sensor (lux)
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
  // Simple timestamp (for demo, using millis)
  // TODO: Add RTC or NTP time synchronization for production
  unsigned long seconds = millis() / 1000;
  char timestamp[32];
  sprintf(timestamp, "ESP32_TIME_%lu", seconds);
  return String(timestamp);
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
