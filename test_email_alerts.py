"""
Test Email Configuration for IoTShield
Run this script to verify Gmail SMTP is working correctly.
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iotshield_backend.settings')
django.setup()

from iotshield_backend.utils.email_alerts import test_email_configuration

if __name__ == "__main__":
    print("\n" + "="*60)
    print("IoTShield Email Configuration Test")
    print("="*60 + "\n")
    
    print("Testing Gmail SMTP connection and email delivery...")
    print("This will send a test email to your configured address.\n")
    
    success = test_email_configuration()
    
    if success:
        print("\n" + "="*60)
        print("✅ SUCCESS! Email configuration is working correctly.")
        print("Check your inbox at: anowar44400@gmail.com")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("❌ FAILED! Email could not be sent.")
        print("Please check your Gmail settings and app password.")
        print("="*60 + "\n")
