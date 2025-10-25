"""Simple MQTT test"""
import paho.mqtt.client as mqtt
import json
import time

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    if reason_code == 0:
        print("✅ Connection successful!")
    else:
        print(f"❌ Connection failed with code {reason_code}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "test_client_123")
client.on_connect = on_connect

try:
    print("Connecting to localhost:1883...")
    client.connect("localhost", 1883, 60)
    client.loop_start()
    
    time.sleep(2)
    
    # Try publishing
    msg = {"test": "data", "value": 42}
    result = client.publish("test/topic", json.dumps(msg))
    print(f"Publish result: {result.rc}")
    
    time.sleep(1)
    client.loop_stop()
    client.disconnect()
    print("✅ Test completed")
    
except Exception as e:
    print(f"❌ Error: {e}")
