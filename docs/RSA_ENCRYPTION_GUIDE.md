# RSA Encryption Implementation Guide for IoTShield

## Overview

This guide explains how to implement end-to-end RSA encryption in IoTShield to secure MQTT payloads between ESP32 devices and the gateway, protecting data even if the MQTT broker is compromised.

---

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   ESP32     │  MQTT   │ MQTT Broker  │  MQTT   │   Gateway   │
│             │ ──────> │ (Untrusted)  │ ──────> │ (Backend)   │
│ Encrypt     │         │              │         │ Decrypt     │
│ (Public Key)│         │ Sees only    │         │ (Private    │
│             │         │ encrypted    │         │  Key)       │
│             │         │ data         │         │             │
└─────────────┘         └──────────────┘         └─────────────┘
```

**Key Points:**
- ESP32 encrypts data with **public key** before publishing
- MQTT broker only sees **encrypted payload**
- Gateway decrypts with **private key**
- TLS protects transport; RSA protects application layer

---

## Backend Setup (Already Implemented)

### 1. Install Dependencies

```bash
pip install pycryptodome
```

### 2. Generate RSA Key Pair

```bash
python manage_rsa_keys.py
```

**Menu Options:**
- **Option 1**: Generate new key pair (2048-bit)
- **Option 2**: Display public key for ESP32
- **Option 4**: Test encryption/decryption

### 3. Export Public Key for ESP32

```bash
# Option 5 in manage_rsa_keys.py exports to docs/rsa_public_key.pem
# Or manually copy from Option 2
```

---

## ESP32 Implementation

### Required Libraries

Add to your `platformio.ini` or Arduino IDE:

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
lib_deps = 
    knolleary/PubSubClient@^2.8
    arduino-libraries/WiFi@^1.2.7
    bblanchon/ArduinoJson@^6.21.3
    rweather/Crypto@^0.4.0  ; For RSA encryption
```

### Public Key Embedding

**Step 1:** Get your public key from backend:
```bash
python manage_rsa_keys.py
# Choose option 2 to display public key
```

**Step 2:** Embed in ESP32 code:

```cpp
// ESP32 Firmware - iotshield_esp32.ino

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Crypto.h>
#include <RSA.h>
#include <RNG.h>
#include <base64.h>

// RSA Public Key (Copy from backend - manage_rsa_keys.py Option 2)
const char* RSA_PUBLIC_KEY = 
"-----BEGIN PUBLIC KEY-----\n"
"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...\n"
"...\n"
"-----END PUBLIC KEY-----";

// RSA Encryption Class
class RSAEncryptor {
private:
    RSAPublicKey publicKey;
    bool initialized = false;
    
public:
    bool begin() {
        // Parse PEM and initialize public key
        // This is simplified - use proper PEM parsing library
        initialized = true;
        return initialized;
    }
    
    String encrypt(String plaintext) {
        if (!initialized) {
            Serial.println("RSA not initialized!");
            return "";
        }
        
        // Convert string to bytes
        uint8_t plainBytes[256];
        plaintext.getBytes(plainBytes, plaintext.length() + 1);
        
        // Encrypt with public key
        uint8_t encryptedBytes[256];
        size_t encryptedLen = 0;
        
        // Perform RSA encryption
        // encryptedLen = rsaEncrypt(publicKey, plainBytes, plaintext.length(), encryptedBytes);
        
        // Convert to base64
        String encrypted = base64::encode(encryptedBytes, encryptedLen);
        
        return encrypted;
    }
};

RSAEncryptor rsaEncryptor;
```

### Sensor Data Encryption

```cpp
// Original sensor reading function
void publishSensorData() {
    // Read sensors
    float temperature = readTemperature();
    float humidity = readHumidity();
    int motion = readMotion();
    
    // Create JSON payload
    StaticJsonDocument<512> doc;
    doc["device_id"] = deviceID;
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["motion"] = motion;
    doc["timestamp"] = getTimestamp();
    
    // Serialize to string
    String plainPayload;
    serializeJson(doc, plainPayload);
    
    // Encrypt payload
    String encryptedData = rsaEncryptor.encrypt(plainPayload);
    
    // Create encrypted MQTT message
    StaticJsonDocument<1024> encryptedDoc;
    encryptedDoc["encrypted"] = true;
    encryptedDoc["encryption_type"] = "RSA-OAEP";
    encryptedDoc["key_size"] = 2048;
    encryptedDoc["data"] = encryptedData;
    
    // Publish encrypted payload
    String encryptedPayload;
    serializeJson(encryptedDoc, encryptedPayload);
    
    mqttClient.publish("iotshield/sensors", encryptedPayload.c_str());
    
    Serial.println("Encrypted data published");
}
```

### Setup Function

```cpp
void setup() {
    Serial.begin(115200);
    
    // Initialize WiFi
    setupWiFi();
    
    // Initialize RSA encryption
    if (rsaEncryptor.begin()) {
        Serial.println("RSA encryption initialized");
    } else {
        Serial.println("RSA encryption failed!");
    }
    
    // Initialize MQTT
    setupMQTT();
}
```

---

## Alternative: Hybrid Encryption (Recommended)

Since RSA can only encrypt **small data** (max ~190 bytes for 2048-bit key), use **hybrid encryption** for larger payloads:

### Hybrid Approach

1. **ESP32:**
   - Generate random AES key (symmetric)
   - Encrypt sensor data with AES
   - Encrypt AES key with RSA
   - Send both encrypted AES key + encrypted data

2. **Gateway:**
   - Decrypt AES key with RSA
   - Decrypt sensor data with AES

```cpp
// ESP32 Hybrid Encryption
String encryptHybrid(String plaintext) {
    // 1. Generate random AES key
    uint8_t aesKey[32]; // 256-bit AES
    generateRandomKey(aesKey, 32);
    
    // 2. Encrypt data with AES
    String encryptedData = aesEncrypt(plaintext, aesKey);
    
    // 3. Encrypt AES key with RSA
    String encryptedKey = rsaEncrypt(aesKey, 32);
    
    // 4. Create hybrid payload
    StaticJsonDocument<2048> doc;
    doc["encrypted"] = true;
    doc["encryption_type"] = "RSA-AES-HYBRID";
    doc["encrypted_key"] = encryptedKey;
    doc["encrypted_data"] = encryptedData;
    
    String payload;
    serializeJson(doc, payload);
    return payload;
}
```

---

## Testing

### 1. Backend Test

```bash
python manage_rsa_keys.py
# Choose Option 4: Test Encryption/Decryption
```

### 2. ESP32 → Gateway Test

**ESP32 Serial Monitor:**
```
Connecting to WiFi...
WiFi connected
RSA encryption initialized
Publishing encrypted sensor data...
✓ Data published successfully
```

**Gateway/Backend Logs:**
```
INFO Received encrypted message on topic iotshield/sensors
DEBUG Data decrypted successfully
INFO Sensor data saved: Device=ESP32_001, Temp=25.5°C
```

### 3. MQTT Broker Verification

Subscribe to MQTT topic and verify data is encrypted:

```bash
mosquitto_sub -h localhost -t "iotshield/sensors" -v
```

**Expected Output (encrypted):**
```json
{
  "encrypted": true,
  "encryption_type": "RSA-OAEP",
  "data": "kJ8mN2pL9xQwV... [base64 encrypted string]"
}
```

---

## Security Best Practices

### Key Management

1. **Private Key Security:**
   - Store private key in `keys/` directory
   - Set permissions: `chmod 600 keys/rsa_private.pem`
   - Never commit to Git (add to `.gitignore`)
   - Use environment variables in production

2. **Public Key Distribution:**
   - Public key can be shared openly
   - Embed in ESP32 firmware
   - Can be stored in device configuration

### Key Rotation

Regenerate keys periodically:

```bash
# Generate new keys
python manage_rsa_keys.py  # Option 1

# Export new public key
python manage_rsa_keys.py  # Option 5

# Update ESP32 firmware with new public key
# Reflash all devices
```

### Limitations

- **RSA Encryption Size:** Max ~190 bytes for 2048-bit key
- **Performance:** RSA is slower than symmetric encryption
- **Recommendation:** Use hybrid encryption for large payloads

---

## Troubleshooting

### Issue: "Data too large for RSA encryption"

**Solution:** Use hybrid encryption (RSA + AES)

### Issue: "Error decrypting data"

**Possible Causes:**
- Wrong key pair
- Corrupted encrypted data
- Key mismatch between ESP32 and gateway

**Solution:**
```bash
# Regenerate keys
python manage_rsa_keys.py  # Option 1

# Re-export public key to ESP32
python manage_rsa_keys.py  # Option 2
```

### Issue: ESP32 crashes during encryption

**Solution:**
- Reduce payload size
- Use hybrid encryption
- Increase ESP32 heap size

---

## Performance Considerations

| Encryption Type | Speed | Payload Size | Security |
|----------------|-------|--------------|----------|
| **No Encryption** | Fast | Unlimited | None |
| **TLS Only** | Fast | Unlimited | Broker sees data |
| **RSA Only** | Slow | ~190 bytes | End-to-end |
| **RSA + AES Hybrid** | Medium | Unlimited | End-to-end |

**Recommendation:** Use RSA + AES Hybrid for production

---

## Files Modified/Created

### Backend Files

 - requirements.txt - Added `pycryptodome`
 - iotshield_backend/privacy_engine.py - Added `RSAEncryption` class
 - iotshield_backend/mqtt_client.py - Added decryption in `on_message()`
 - iotshield_backend/settings.py - Added RSA settings
 - manage_rsa_keys.py - Key management script (NEW)
 - docs/RSA_ENCRYPTION_GUIDE.md - This guide (NEW)

### ESP32 Files (To Be Modified)

- ⏳ `edge_integration/firmware/iotshield_esp32/iotshield_esp32.ino`
  - Add RSA encryption before MQTT publish
  - Embed public key

---

## Next Steps

 1. Backend implementation complete
 2. Install dependencies: `pip install -r requirements.txt`
 3. Generate RSA keys: `python manage_rsa_keys.py`
 4. Test encryption: Run Option 4 in key manager
 5. Implement ESP32 encryption (see code examples above)
 6. Test end-to-end encryption
 7. (Optional) Implement hybrid encryption for larger payloads

---

## Additional Resources

- **PyCryptodome Documentation:** https://pycryptodome.readthedocs.io/
- **ESP32 Crypto Library:** https://github.com/rweather/arduinolibs
- **MQTT Security Best Practices:** OWASP IoT Project

---

## Support

If you encounter issues:
1. Check logs: `tail -f iotshield.log`
2. Test with key manager: `python manage_rsa_keys.py`
3. Verify keys exist: `ls -la keys/`
4. Check Django settings for RSA configuration

---

**Document Version:** 1.0  
**Last Updated:** February 17, 2026  
**Authors:** IoTShield Team
