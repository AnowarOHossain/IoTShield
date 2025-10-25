"""
IoT Sensor Simulator for IoTShield
Simulates ESP32 sensor data and publishes to MQTT broker
"""
import json
import time
import random
import logging
import os
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

# Import simulator utilities
from utils.sensors import SensorSimulator
from utils.mqtt_publisher import MQTTPublisher
from utils.logger import setup_logger

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# Setup logging
logger = setup_logger('simulator')


class IoTDeviceSimulator:
    """Simulates IoT device with multiple sensors"""
    
    def __init__(self, device_config):
        self.device_id = device_config['device_id']
        self.device_name = device_config['device_name']
        self.device_type = device_config.get('device_type', 'SIMULATOR')
        self.location = device_config.get('location', 'Unknown')
        
        # Initialize sensors - pass config dict
        self.sensor_simulator = SensorSimulator(config)
        
        # Initialize MQTT publisher
        self.mqtt_publisher = MQTTPublisher(
            broker_host=config['mqtt']['broker_host'],
            broker_port=config['mqtt']['broker_port'],
            client_id=self.device_id
        )
        
        # Simulation parameters
        self.publish_interval = device_config.get('publish_interval', 5)
        self.is_running = False
        
        logger.info(f"Initialized device simulator: {self.device_name} ({self.device_id})")
    
    def start(self):
        """Start the simulation"""
        self.is_running = True
        logger.info(f"Starting simulation for {self.device_name}")
        
        # Connect to MQTT broker
        self.mqtt_publisher.connect()
        
        # Wait for connection to establish
        logger.info("Waiting for MQTT connection...")
        time.sleep(2)  # Give time for async connection
        
        try:
            while self.is_running:
                self.publish_sensor_data()
                time.sleep(self.publish_interval)
        
        except KeyboardInterrupt:
            logger.info("Simulation interrupted by user")
        
        finally:
            self.stop()
    
    def stop(self):
        """Stop the simulation"""
        self.is_running = False
        self.mqtt_publisher.disconnect()
        logger.info(f"Stopped simulation for {self.device_name}")
    
    def publish_sensor_data(self):
        """Generate and publish sensor data"""
        # Generate sensor readings
        temperature = self.sensor_simulator.read_temperature()
        humidity = self.sensor_simulator.read_humidity()
        gas = self.sensor_simulator.read_gas()
        flame = self.sensor_simulator.read_flame()
        motion = self.sensor_simulator.read_motion()
        light = self.sensor_simulator.read_light()
        
        # Publish each sensor reading
        sensors = [
            ('TEMPERATURE', temperature, '°C'),
            ('HUMIDITY', humidity, '%'),
            ('GAS', gas, 'ppm'),
            ('FLAME', flame, ''),
            ('MOTION', motion, ''),
            ('LIGHT', light, 'lux'),
        ]
        
        for sensor_type, value, unit in sensors:
            message = {
                'device_id': self.device_id,
                'device_name': self.device_name,
                'device_type': self.device_type,
                'sensor_type': sensor_type,
                'value': value,
                'unit': unit,
                'location': self.location,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            
            # Publish to MQTT
            success = self.mqtt_publisher.publish(
                config['mqtt']['topic_sensors'],
                message
            )
            
            if success:
                logger.debug(f"Published {sensor_type}: {value}{unit}")
            else:
                logger.error(f"Failed to publish {sensor_type}")


def main():
    """Main simulation entry point"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║         IoTShield Sensor Simulator v1.0              ║
    ║   Privacy-Preserving IoT Monitoring System           ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Get device configuration
    device_config = config['device']
    
    # Create and start simulator
    simulator = IoTDeviceSimulator(device_config)
    
    try:
        logger.info("=" * 60)
        logger.info("Starting IoTShield Sensor Simulator")
        logger.info(f"Device ID: {device_config['device_id']}")
        logger.info(f"Device Name: {device_config['device_name']}")
        logger.info(f"Publish Interval: {device_config.get('publish_interval', 5)} seconds")
        logger.info(f"MQTT Broker: {config['mqtt']['broker_host']}:{config['mqtt']['broker_port']}")
        logger.info("=" * 60)
        logger.info("Press Ctrl+C to stop the simulator")
        logger.info("=" * 60)
        
        simulator.start()
    
    except Exception as e:
        logger.error(f"Simulation error: {e}")
        raise


if __name__ == '__main__':
    main()
