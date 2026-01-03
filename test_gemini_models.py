"""
Test script to list available Gemini models
"""
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=api_key)

print("=" * 60)
print("Available Gemini Models:")
print("=" * 60)

try:
    models = genai.list_models()
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Methods: {', '.join(model.supported_generation_methods)}")
            print()
except Exception as e:
    print(f"ERROR: {e}")
    print("\nTrying alternate method...")
    try:
        # Try with gemini-pro first
        test_model = genai.GenerativeModel('gemini-pro')
        response = test_model.generate_content("Say 'Hello'")
        print("✓ gemini-pro is working!")
        print(f"Response: {response.text}")
    except Exception as e2:
        print(f"ERROR with gemini-pro: {e2}")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)
