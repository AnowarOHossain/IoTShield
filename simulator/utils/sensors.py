"""Sensor data generators"""

import random
import json
import os


class SensorSimulator:
    """Simulates various IoT sensors"""
    
    def __init__(self, config_file='config.json'):
        # Handle both string path and dict config
        if isinstance(config_file, dict):
            config = config_file
        else:
            # If it's a relative path, make it relative to simulator directory
            if not os.path.isabs(config_file):
                config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_file)
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
            # Generate anomalies across different severity ranges
            severity_roll = random.random()
            if severity_roll < 0.15:  # 15% CRITICAL
                value = random.uniform(0.76, 0.90)  # Critical gas leak
            elif severity_roll < 0.40:  # 25% HIGH
                value = random.uniform(0.66, 0.75)  # High gas level
            elif severity_roll < 0.70:  # 30% MEDIUM
                value = random.uniform(0.51, 0.65)  # Medium gas level
            else:  # 30% LOW
                value = random.uniform(0.36, 0.50)  # Slightly elevated
        
        # Clamp value BEFORE adding noise to prevent overflow
        value = max(0, min(0.95, value))
        
        # Add privacy noise (smaller amount to prevent overflow)
        if self.privacy_config.get('enable_noise', False):
            epsilon = self.privacy_config.get('noise_epsilon', 0.5)
            # Reduce noise impact for bounded values
            noise = random.gauss(0, 0.01 / epsilon)  # Much smaller noise
            value = value + noise
        
        return round(max(0, min(0.95, value)), 3)
    
    def read_flame(self):
        """Simulate flame sensor (0-1 continuous value)"""
        config = self.sensor_config.get('flame', {})
        anomaly_chance = config.get('anomaly_chance', 0.01)
        
        # Usually 0, rarely detect flame with varying intensity
        if random.random() < anomaly_chance:
            # Flame detected - vary by severity
            severity_roll = random.random()
            if severity_roll < 0.2:  # 20% CRITICAL - actual fire
                value = random.uniform(0.71, 0.95)
            elif severity_roll < 0.5:  # 30% HIGH - strong heat signature
                value = random.uniform(0.56, 0.70)
            elif severity_roll < 0.75:  # 25% MEDIUM - notable heat
                value = random.uniform(0.36, 0.55)
            else:  # 25% LOW - minor heat signature
                value = random.uniform(0.16, 0.35)
        else:
            # Normal - very low or no flame
            value = random.uniform(0, 0.10)
        
        return round(value, 2)
    
    def read_motion(self):
        """Simulate motion sensor (0-1 continuous value)"""
        config = self.sensor_config.get('motion', {})
        activity_chance = config.get('activity_chance', 0.3)
        
        # Generate motion intensity instead of binary
        if random.random() < activity_chance:
            # Motion detected - vary intensity
            base_intensity = config.get('base_intensity', 0.3)
            value = random.uniform(base_intensity * 0.5, base_intensity * 2)
            
            # Rare high-intensity motion
            if random.random() < 0.05:
                value = random.uniform(0.7, 0.95)
        else:
            # No motion or very low
            value = random.uniform(0, 0.15)
        
        return round(max(0, min(1, value)), 2)
    
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
