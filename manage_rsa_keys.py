#!/usr/bin/env python
"""
RSA Key Management Script for IoTShield

This is a simple tool to help you manage encryption keys.
Run this script to generate keys, view them, or test encryption.
"""
import os
import sys
import django
from pathlib import Path

# Set up Django so we can use IoTShield settings and models
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iotshield_backend.settings')
django.setup()

from iotshield_backend.privacy_engine import RSAEncryption
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def display_menu():
    """Display management menu"""
    print("\n" + "="*60)
    print("       IoTShield RSA Key Management")
    print("="*60)
    print("1. Generate New RSA Key Pair")
    print("2. Display Public Key (for IoT devices)")
    print("3. View Key Information")
    print("4. Test Encryption/Decryption")
    print("5. Export Public Key to File")
    print("6. Exit")
    print("="*60)


def generate_keys():
    """Create a brand new pair of RSA keys"""
    print("\n[WARNING] This will overwrite existing keys!")
    confirm = input("Are you sure you want to generate new keys? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        return
    
    try:
        # Create RSA encryption object and generate keys
        rsa = RSAEncryption()
        rsa.generate_keys()
        print(f"\n[SUCCESS] New {rsa.key_size}-bit RSA key pair generated!")
        print(f"  Private Key: {rsa.private_key_path}")
        print(f"  Public Key: {rsa.public_key_path}")
    except Exception as e:
        print(f"[ERROR] Error generating keys: {e}")


def display_public_key():
    """Show the public key that needs to go on ESP32 devices"""
    try:
        rsa = RSAEncryption()
        public_key_pem = rsa.get_public_key_pem()
        
        print("\n" + "="*60)
        print("PUBLIC KEY (Copy this to your IoT devices)")
        print("="*60)
        print(public_key_pem)
        print("="*60)
        print("\nThis key should be embedded in your ESP32 firmware.")
    except Exception as e:
        print(f"[ERROR] Error reading public key: {e}")


def view_key_info():
    """Display details about the current keys"""
    try:
        rsa = RSAEncryption()
        
        print("\n" + "="*60)
        print("RSA KEY INFORMATION")
        print("="*60)
        print(f"Key Size: {rsa.key_size} bits")
        print(f"Private Key Path: {rsa.private_key_path}")
        print(f"Public Key Path: {rsa.public_key_path}")
        print(f"Private Key Exists: {rsa.private_key_path.exists()}")
        print(f"Public Key Exists: {rsa.public_key_path.exists()}")
        
        # Check if keys are loaded and working
        if rsa.private_key:
            print(f"Private Key Loaded: Yes")
            print(f"Can Decrypt: Yes")
        else:
            print(f"Private Key Loaded: No")
        
        if rsa.public_key:
            print(f"Public Key Loaded: Yes")
            print(f"Can Encrypt: Yes")
        else:
            print(f"Public Key Loaded: No")
        
        print("="*60)
    except Exception as e:
        print(f"[ERROR] Error reading key info: {e}")


def test_encryption():
    """Run a test to make sure encryption and decryption work correctly"""
    try:
        rsa = RSAEncryption()
        
        # Sample sensor data to test with
        test_data = {
            "device_id": "ESP32_TEST_001",
            "temperature": 25.5,
            "humidity": 60.0,
            "timestamp": "2026-02-17T10:30:00Z"
        }
        
        print("\n" + "="*60)
        print("ENCRYPTION TEST")
        print("="*60)
        print(f"Original Data: {test_data}")
        
        # Step 1: Encrypt the test data
        encrypted = rsa.encrypt_mqtt_payload(test_data)
        print(f"\nEncrypted Payload:")
        print(f"  Type: {encrypted.get('encryption_type')}")
        print(f"  Encrypted: {encrypted.get('encrypted')}")
        print(f"  Data (truncated): {encrypted.get('data')[:50]}...")
        
        # Step 2: Decrypt it back
        decrypted = rsa.decrypt_mqtt_payload(encrypted)
        print(f"\nDecrypted Data: {decrypted}")
        
        # Step 3: Check if we got the same data back
        if test_data == decrypted:
            print("\n[SUCCESS] Encryption/Decryption test PASSED!")
        else:
            print("\n[FAILED] Encryption/Decryption test FAILED!")
            print(f"Expected: {test_data}")
            print(f"Got: {decrypted}")
        
        print("="*60)
    except Exception as e:
        print(f"[ERROR] Error during test: {e}")


def export_public_key():
    """Save the public key to a file for easy sharing with devices"""
    try:
        rsa = RSAEncryption()
        
        # Save to docs folder where it's easy to find
        output_path = BASE_DIR / 'docs' / 'rsa_public_key.pem'
        
        with open(output_path, 'w') as f:
            f.write(rsa.get_public_key_pem())
        
        print(f"\n[SUCCESS] Public key exported to: {output_path}")
        print("  You can share this file with your IoT devices.")
    except Exception as e:
        print(f"[ERROR] Error exporting public key: {e}")


def main():
    """Main loop - shows menu and handles user choices"""
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        # Handle each menu option
        if choice == '1':
            generate_keys()
        elif choice == '2':
            display_public_key()
        elif choice == '3':
            view_key_info()
        elif choice == '4':
            test_encryption()
        elif choice == '5':
            export_public_key()
        elif choice == '6':
            print("\nExiting...")
            break
        else:
            print("\n[ERROR] Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        sys.exit(1)
