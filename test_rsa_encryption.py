#!/usr/bin/env python
"""
Quick RSA Encryption Test for IoTShield
Tests the RSA implementation without Django
"""
import os
import sys
import json
import base64
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

try:
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
    print("[OK] pycryptodome imported successfully")
except ImportError:
    print("[ERROR] pycryptodome not installed. Run: python -m pip install pycryptodome")
    sys.exit(1)


def quick_test():
    """Quick RSA encryption test"""
    print("\n" + "="*60)
    print("IoTShield RSA Encryption - Quick Test")
    print("="*60)
    
    # Generate keys
    print("\n1. Generating RSA key pair (2048-bit)...")
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()
    print("   [OK] Key pair generated")
    
    # Test data
    test_data = {
        "device_id": "ESP32_TEST_001",
        "temperature": 25.5,
        "humidity": 60.0,
        "timestamp": "2026-02-17T10:30:00Z"
    }
    
    print(f"\n2. Original Data:")
    print(f"   {test_data}")
    
    # Encrypt
    print("\n3. Encrypting data...")
    cipher_encrypt = PKCS1_OAEP.new(public_key)
    json_data = json.dumps(test_data)
    encrypted = cipher_encrypt.encrypt(json_data.encode('utf-8'))
    encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
    print(f"   [OK] Data encrypted ({len(encrypted)} bytes)")
    print(f"   Base64: {encrypted_b64[:50]}...")
    
    # Decrypt
    print("\n4. Decrypting data...")
    cipher_decrypt = PKCS1_OAEP.new(private_key)
    decrypted = cipher_decrypt.decrypt(encrypted)
    decrypted_data = json.loads(decrypted.decode('utf-8'))
    print(f"   [OK] Data decrypted")
    print(f"   {decrypted_data}")
    
    # Verify
    print("\n5. Verification:")
    if test_data == decrypted_data:
        print("   [SUCCESS] Encryption/Decryption working correctly!")
    else:
        print("   [FAILED] Data mismatch!")
        return False
    
    # Create MQTT-style payload
    print("\n6. MQTT Payload Format:")
    mqtt_payload = {
        "encrypted": True,
        "encryption_type": "RSA-OAEP",
        "key_size": 2048,
        "data": encrypted_b64
    }
    print(f"   {json.dumps(mqtt_payload, indent=2)[:200]}...")
    
    print("\n" + "="*60)
    print("[SUCCESS] All tests passed! RSA encryption is working.")
    print("="*60)
    
    return True


if __name__ == "__main__":
    try:
        quick_test()
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
