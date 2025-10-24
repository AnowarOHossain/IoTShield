#!/bin/bash
# Script to run MQTT broker (Mosquitto)

echo "Starting Mosquitto MQTT Broker..."

# Check if mosquitto is installed
if ! command -v mosquitto &> /dev/null; then
    echo "Mosquitto is not installed!"
    echo "Install it using:"
    echo "  Ubuntu/Debian: sudo apt-get install mosquitto mosquitto-clients"
    echo "  macOS: brew install mosquitto"
    echo "  Windows: Download from https://mosquitto.org/download/"
    exit 1
fi

# Start mosquitto broker
mosquitto -v -p 1883
