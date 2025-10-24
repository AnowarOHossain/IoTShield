"""Sensor data generators"""

import random
import json


class SensorSimulator:
    """Simulates various IoT sensors"""
    
    def __init__(self, config_file='config.json'):
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        self.sensor_config = config.get('sensors', {})
        self.privacy_config = config.get('privacy', {})
    
    def read_temperature(self):
        """Simulate temperature sensor (°C)"""
        config = self.sensor_config.get('temperature', {})
        base = config.get('base_value', 25)
        variance = config.get('variance', 3)
        anomaly_chance = config.get('anomaly_chance', 0.05)
        
        # Normal reading
        value = random.normalvariate(base, variance)
        
        # Occasionally generate anomalies
        if random.random() < anomaly_chance:
            value = random.choice([
                random.uniform(40, 50),  # High temperature
                random.uniform(5, 15),   # Low temperature
            ])
        
        # Add privacy noise
        if self.privacy_config.get('enable_noise', False):
            value = self._add_noise(value)
        
        return round(value, 2)
    
    def read_humidity(self):
        """Simulate humidity sensor (%)"""
        config = self.sensor_config.get('humidity', {})
        base = config.get('base_value', 60)
        variance = config.get('variance', 10)
        anomaly_chance = config.get('anomaly_chance', 0.05)
        
        value = random.normalvariate(base, variance)
        
        if random.random() < anomaly_chance:
            value = random.uniform(85, 95)  # High humidity
        
        if self.privacy_config.get('enable_noise', False):
            value = self._add_noise(value)
        
        return round(max(0, min(100, value)), 2)
    
    def read_gas(self):
        """Simulate gas sensor (ppm normalized 0-1)"""
        config = self.sensor_config.get('gas', {})
        base = config.get('base_value', 0.1)
        variance = config.get('variance', 0.05)
        anomaly_chance = config.get('anomaly_chance', 0.02)
        
        value = random.normalvariate(base, variance)
        
        if random.random() < anomaly_chance:
            value = random.uniform(0.7, 0.95)  # Gas leak!
        
        if self.privacy_config.get('enable_noise', False):
            value = self._add_noise(value)
        
        return round(max(0, min(1, value)), 3)
    
    def read_flame(self):
        """Simulate flame sensor (binary 0/1)"""
        config = self.sensor_config.get('flame', {})
        anomaly_chance = config.get('anomaly_chance', 0.01)
        
        # Usually 0, rarely 1 (fire!)
        value = 1 if random.random() < anomaly_chance else 0
        
        return value
    
    def read_motion(self):
        """Simulate motion sensor (binary 0/1)"""
        config = self.sensor_config.get('motion', {})
        activity_chance = config.get('activity_chance', 0.3)
        
        value = 1 if random.random() < activity_chance else 0
        
        return value
    
    def read_light(self):
        """Simulate light sensor (lux)"""
        config = self.sensor_config.get('light', {})
        base = config.get('base_value', 300)
        variance = config.get('variance', 100)
        anomaly_chance = config.get('anomaly_chance', 0.03)
        
        value = random.normalvariate(base, variance)
        
        if random.random() < anomaly_chance:
            value = random.choice([
                random.uniform(0, 50),      # Very dark
                random.uniform(900, 1500),  # Very bright
            ])
        
        if self.privacy_config.get('enable_noise', False):
            value = self._add_noise(value)
        
        return round(max(0, value), 2)
    
    def _add_noise(self, value):
        """Add privacy-preserving noise"""
        epsilon = self.privacy_config.get('noise_epsilon', 0.5)
        noise_type = self.privacy_config.get('noise_type', 'gaussian')
        
        if noise_type == 'gaussian':
            noise = random.gauss(0, 1/epsilon)
        else:  # laplace
            noise = random.expovariate(epsilon) * random.choice([-1, 1])
        
        return value + noise
