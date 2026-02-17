# RSA Encryption for IoTShield - Quick Start

## Overview

RSA end-to-end encryption has been implemented to secure MQTT payloads between ESP32 devices and the IoTShield backend gateway. This protects data even if the MQTT broker is compromised.

## What Was Implemented

### 1. Backend Components

 - **RSA Encryption Class** (`privacy_engine.py`)
   - Key generation (2048-bit or 4096-bit)
   - Encryption/Decryption methods
   - MQTT payload handling
   - Automatic key loading/saving

 - **MQTT Client Integration** (`mqtt_client.py`)
   - Automatic decryption of incoming encrypted messages
   - Seamless integration with existing workflow

 - **Key Management Script** (`manage_rsa_keys.py`)
   - Interactive CLI for key management
   - Key generation, viewing, export
   - Encryption testing

 - **Security Configuration**
   - RSA settings in `settings.py`
   - Keys stored securely in `keys/` directory
   - `.gitignore` updated to exclude private keys
 - Added `pycryptodome==3.21.0` to `requirements.txt`
 - **Complete Implementation Guide** (`docs/RSA_ENCRYPTION_GUIDE.md`)

### 2. Dependencies

-  Added `pycryptodome==3.21.0` to `requirements.txt`

### 3. Documentation

-  **Complete Implementation Guide** (`docs/RSA_ENCRYPTION_GUIDE.md`)
  - Architecture overview
  - Backend setup instructions
  - ESP32 implementation guide
  - Testing procedures
  - Security best practices

---

## Quick Start

### Step 1: Install Dependencies

```bash
python -m pip install pycryptodome
# Or install all requirements:
python -m pip install -r requirements.txt
```

### Step 2: Generate RSA Keys

```bash
python manage_rsa_keys.py
```

**Menu Options:**
1. Generate New RSA Key Pair (Choose this first)
2. Display Public Key (for IoT devices)
3. View Key Information
4. Test Encryption/Decryption (Run this to verify)
5. Export Public Key to File
6. Exit

### Step 3: Test Implementation

**Quick Test (without Django):**
```bash
python test_rsa_encryption.py
```

**Full Test (with Django):**
```bash
python manage_rsa_keys.py
# Choose Option 4: Test Encryption/Decryption
```

Expected output:
```
Encryption/Decryption test PASSED!
```

### Step 4: Get Public Key for ESP32

```bash
python manage_rsa_keys.py
# Choose Option 2 to display public key
# Or Option 5 to export to docs/rsa_public_key.pem
```

Copy the public key and embed it in your ESP32 firmware.

---

## Architecture

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────────┐
│   ESP32 Device  │  MQTT   │ MQTT Broker  │  MQTT   │  IoTShield      │
│                 │ ──────> │ (Untrusted)  │ ──────> │  Gateway        │
│                 │         │              │         │                 │
│ Encrypt with    │         │ Sees only    │         │ Decrypt with    │
│ PUBLIC KEY      │         │ encrypted    │         │ PRIVATE KEY     │
│                 │         │ data        │         │                 │
└─────────────────┘         └──────────────┘         └─────────────────┘
```

**Security Benefits:**
 - End-to-end encryption
 - MQTT broker cannot read data
 - Protection against man-in-the-middle attacks
 - Additional layer on top of TLS

---

## Files Created/Modified

### Created Files

| File | Purpose |
|------|---------|
| `manage_rsa_keys.py` | Interactive key management CLI |
| `test_rsa_encryption.py` | Quick standalone encryption test |
| `docs/RSA_ENCRYPTION_GUIDE.md` | Complete implementation guide |
| `docs/RSA_QUICK_START.md` | This file |

### Modified Files

| File | Changes |
|------|---------|
| `requirements.txt` | Added `pycryptodome==3.21.0` |
| `iotshield_backend/privacy_engine.py` | Added `RSAEncryption` class |
| `iotshield_backend/mqtt_client.py` | Added automatic decryption |
| `iotshield_backend/settings.py` | Added RSA configuration |
| `.gitignore` | Added `keys/` directory exclusion |

### Auto-Generated Files (After Running)

| File | Description |
|------|-------------|
| `keys/rsa_private.pem` | Private key (KEEP SECRET!) |
| `keys/rsa_public.pem` | Public key (share with devices) |
| `docs/rsa_public_key.pem` | Exported public key |

---

## Usage Examples

### Backend (Automatic Decryption)

The MQTT client automatically decrypts incoming messages:

```python
# mqtt_client.py (already implemented)
def on_message(self, client, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))
    
    # Automatic decryption
    from .privacy_engine import rsa_encryption
    if rsa_encryption:
        data = rsa_encryption.decrypt_mqtt_payload(data)
    
    # Process decrypted data
    self.handle_sensor_data(data)
```

### ESP32 (Manual Implementation Needed)

See `docs/RSA_ENCRYPTION_GUIDE.md` for complete ESP32 implementation guide.

**Basic flow:**
1. Embed public key in firmware
2. Read sensor data
3. Encrypt JSON payload with public key
4. Publish encrypted payload to MQTT

---

## Testing Checklist

- [ ] Install `pycryptodome`: `python -m pip install pycryptodome`
- [ ] Generate keys: `python manage_rsa_keys.py` → Option 1
- [ ] Test encryption: `python test_rsa_encryption.py`
- [ ] Verify keys exist: `ls keys/` (should see `rsa_private.pem` and `rsa_public.pem`)
- [ ] Export public key: `python manage_rsa_keys.py` → Option 5
- [ ] (Optional) Test with Django: `python manage_rsa_keys.py` → Option 4

---

## Security Notes

### CRITICAL: Private Key Security

**The private key (`keys/rsa_private.pem`) is SENSITIVE!**

 - NEVER commit to Git (already in `.gitignore`)
 - NEVER share or expose publicly
 - Keep in secure location
 - Set restrictive file permissions: `chmod 600 keys/rsa_private.pem`
 - Backup securely (encrypted storage)

### Public Key Distribution

The public key (`keys/rsa_public.pem`) can be shared:
 - Embed in ESP32 firmware
 - Store in device configuration
 - Distribute to all IoT devices

### Key Rotation

Recommended to rotate keys periodically:

```bash
# 1. Generate new keys
python manage_rsa_keys.py (Option 1)
# 2. Export new public key
python manage_rsa_keys.py (Option 5)
# 3. Update all ESP32 devices with new public key
# 4. Reflash all devices
```

---

## Limitations & Recommendations

### RSA Limitations

- **Payload Size:** RSA can only encrypt ~190 bytes (for 2048-bit key)
- **Performance:** RSA is computationally expensive
- **ESP32 Memory:** Limited heap for encryption operations

### Recommended Approach: Hybrid Encryption

For larger payloads, use **RSA + AES hybrid encryption**:

1. ESP32 generates random AES key
2. Encrypt data with AES (fast, unlimited size)
3. Encrypt AES key with RSA
4. Send both encrypted AES key + encrypted data

See `docs/RSA_ENCRYPTION_GUIDE.md` for hybrid implementation details.

---

## Troubleshooting

### Issue: "Module 'Crypto' not found"

**Solution:**
```bash
python -m pip install pycryptodome
```

### Issue: "KeyError: RSA_ENCRYPTION_ENABLED"

**Solution:** Add to `settings.py` (already added):
```python
RSA_ENCRYPTION_ENABLED = True
RSA_KEY_SIZE = 2048
```

### Issue: "Error decrypting data"

**Possible causes:**
- Different keys on ESP32 and gateway
- Corrupted encrypted data
- Wrong encryption format

**Solution:**
1. Regenerate keys: `python manage_rsa_keys.py` → Option 1
2. Re-export public key: `python manage_rsa_keys.py` → Option 2
3. Update ESP32 firmware with new key

### Issue: "Data too large for RSA encryption"

**Solution:** Implement hybrid encryption (see guide)

---

## Next Steps

1. Backend implementation COMPLETE
2. Install dependencies and test
3. Implement ESP32 encryption (see `docs/RSA_ENCRYPTION_GUIDE.md`)
4. Test end-to-end encryption
5. (Optional) Implement hybrid encryption for larger payloads
6. Deploy to production

---

## Additional Resources

- **Full Implementation Guide:** `docs/RSA_ENCRYPTION_GUIDE.md`
- **PyCryptodome Docs:** https://pycryptodome.readthedocs.io/
- **ESP32 Crypto Library:** https://github.com/rweather/arduinolibs

---

## Support

For issues or questions:
1. Check logs: `tail -f iotshield.log`
2. Run tests: `python test_rsa_encryption.py`
3. Verify configuration: `python manage_rsa_keys.py` → Option 3

---

**Status:** Backend Implementation Complete  
**Version:** 1.0  
**Last Updated:** February 17, 2026
