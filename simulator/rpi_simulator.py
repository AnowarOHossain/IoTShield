"""
IoT Sensor Simulator for IoTShield - Raspberry Pi Version
Simulates Raspberry Pi Edge Gateway with multiple sensors
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

# Load Raspberry Pi configuration
config_path = os.path.join(os.path.dirname(__file__), 'rpi_config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# Setup logging
logger = setup_logger('rpi_simulator')


class RaspberryPiSimulator:
    """Simulates Raspberry Pi Edge Gateway with multiple sensors"""
    
    def __init__(self, device_config):
        self.device_id = device_config['device_id']
        self.device_name = device_config['device_name']
        self.device_type = device_config.get('device_type', 'RASPBERRY_PI')
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
        
        # RPI-specific features
        self.cpu_temp_base = 45.0  # Base CPU temperature
        self.memory_usage_base = 35.0  # Base memory usage %
        
        logger.info(f"Initialized Raspberry Pi simulator: {self.device_name} ({self.device_id})")
    
    def start(self):
        """Start the simulation"""
        self.is_running = True
        logger.info(f"Starting Raspberry Pi simulation for {self.device_name}")
        
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
        logger.info(f"Stopped Raspberry Pi simulation for {self.device_name}")
    
    def read_cpu_temperature(self):
        """Simulate Raspberry Pi CPU temperature"""
        # Normal range: 40-55°C
        variance = random.uniform(-5, 10)
        temp = self.cpu_temp_base + variance
        
        # Occasional anomaly (thermal throttling)
        if random.random() < 0.02:  # 2% chance
            temp = random.uniform(75, 85)
        
        return round(temp, 2)
    
    def read_memory_usage(self):
        """Simulate Raspberry Pi memory usage percentage"""
        # Normal range: 20-50%
        variance = random.uniform(-15, 15)
        usage = self.memory_usage_base + variance
        
        # Occasional high usage
        if random.random() < 0.03:  # 3% chance
            usage = random.uniform(85, 95)
        
        return round(max(0, min(100, usage)), 2)
    
    def read_disk_usage(self):
        """Simulate disk usage percentage"""
        # Simulating slowly increasing disk usage
        base = 45.0
        variance = random.uniform(-2, 3)
        usage = base + variance
        
        return round(max(0, min(100, usage)), 2)
    
    def publish_sensor_data(self):
        """Generate and publish sensor data"""
        # Generate environmental sensor readings
        temperature = self.sensor_simulator.read_temperature()
        humidity = self.sensor_simulator.read_humidity()
        gas = self.sensor_simulator.read_gas()
        flame = self.sensor_simulator.read_flame()
        motion = self.sensor_simulator.read_motion()
        light = self.sensor_simulator.read_light()
        
        # Generate Raspberry Pi system metrics
        cpu_temp = self.read_cpu_temperature()
        memory_usage = self.read_memory_usage()
        disk_usage = self.read_disk_usage()
        
        # Publish environmental sensors
        env_sensors = [
            ('TEMPERATURE', temperature, '°C'),
            ('HUMIDITY', humidity, '%'),
            ('GAS', gas, 'ppm'),
            ('FLAME', flame, ''),
            ('MOTION', motion, ''),
            ('LIGHT', light, 'lux'),
        ]
        
        # Publish system metrics
        system_metrics = [
            ('CPU_TEMPERATURE', cpu_temp, '°C'),
            ('MEMORY_USAGE', memory_usage, '%'),
            ('DISK_USAGE', disk_usage, '%'),
        ]
        
        # Combine all sensors
        all_sensors = env_sensors + system_metrics
        
        for sensor_type, value, unit in all_sensors:
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
    ║    IoTShield Raspberry Pi Simulator v1.0             ║
    ║   Edge Gateway with Enhanced Monitoring              ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Get device configuration
    device_config = config['device']
    
    # Create and start simulator
    simulator = RaspberryPiSimulator(device_config)
    
    try:
        logger.info("=" * 60)
        logger.info("Starting IoTShield Raspberry Pi Simulator")
        logger.info(f"Device ID: {device_config['device_id']}")
        logger.info(f"Device Name: {device_config['device_name']}")
        logger.info(f"Device Type: Raspberry Pi Edge Gateway")
        logger.info(f"Publish Interval: {device_config.get('publish_interval', 5)} seconds")
        logger.info(f"MQTT Broker: {config['mqtt']['broker_host']}:{config['mqtt']['broker_port']}")
        logger.info("=" * 60)
        logger.info("Monitoring: Environmental sensors + System metrics")
        logger.info("Press Ctrl+C to stop the simulator")
        logger.info("=" * 60)
        
        simulator.start()
    
    except Exception as e:
        logger.error(f"Simulation error: {e}")
        raise


if __name__ == '__main__':
    main()
