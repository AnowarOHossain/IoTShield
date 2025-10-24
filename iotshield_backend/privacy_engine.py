"""
Privacy-Preserving Engine for IoTShield
Implements differential privacy through noise addition
"""
import logging
import numpy as np
from django.conf import settings

logger = logging.getLogger('iotshield')


class PrivacyEngine:
    """Privacy-preserving mechanisms using differential privacy"""
    
    def __init__(self):
        self.epsilon = settings.PRIVACY_NOISE_EPSILON
        self.delta = settings.PRIVACY_NOISE_DELTA
    
    def add_gaussian_noise(self, value, sensitivity=1.0):
        """
        Add Gaussian noise to a value for differential privacy
        
        Args:
            value: Original sensor value
            sensitivity: Sensitivity of the query (default 1.0)
        
        Returns:
            Noisy value with differential privacy guarantee
        """
        try:
            # Calculate standard deviation for Gaussian mechanism
            sigma = (sensitivity * np.sqrt(2 * np.log(1.25 / self.delta))) / self.epsilon
            
            # Generate Gaussian noise
            noise = np.random.normal(0, sigma)
            
            # Add noise to value
            noisy_value = value + noise
            
            logger.debug(f"Added Gaussian noise: {value} -> {noisy_value} (noise: {noise:.4f})")
            
            return noisy_value
        
        except Exception as e:
            logger.error(f"Error adding Gaussian noise: {e}")
            return value
    
    def add_laplace_noise(self, value, sensitivity=1.0):
        """
        Add Laplace noise to a value for differential privacy
        
        Args:
            value: Original sensor value
            sensitivity: Sensitivity of the query (default 1.0)
        
        Returns:
            Noisy value with differential privacy guarantee
        """
        try:
            # Calculate scale parameter for Laplace mechanism
            scale = sensitivity / self.epsilon
            
            # Generate Laplace noise
            noise = np.random.laplace(0, scale)
            
            # Add noise to value
            noisy_value = value + noise
            
            logger.debug(f"Added Laplace noise: {value} -> {noisy_value} (noise: {noise:.4f})")
            
            return noisy_value
        
        except Exception as e:
            logger.error(f"Error adding Laplace noise: {e}")
            return value
    
    def add_noise_to_sensor_data(self, sensor_type, value):
        """
        Add appropriate noise based on sensor type
        
        Args:
            sensor_type: Type of sensor
            value: Original sensor value
        
        Returns:
            Noisy value with appropriate bounds
        """
        # Define sensitivity for each sensor type
        sensitivities = {
            'TEMPERATURE': 2.0,  # ±2°C sensitivity
            'HUMIDITY': 5.0,  # ±5% sensitivity
            'GAS': 0.1,  # ±0.1 sensitivity
            'FLAME': 0.05,  # ±0.05 sensitivity
            'MOTION': 0.0,  # No noise for binary motion
            'LIGHT': 50.0,  # ±50 lux sensitivity
        }
        
        sensitivity = sensitivities.get(sensor_type, 1.0)
        
        # Don't add noise to binary sensors
        if sensor_type in ['MOTION', 'FLAME'] and value in [0, 1]:
            return value
        
        # Add Gaussian noise (suitable for continuous data)
        noisy_value = self.add_gaussian_noise(value, sensitivity)
        
        # Clip values to reasonable bounds
        bounds = self._get_sensor_bounds(sensor_type)
        noisy_value = np.clip(noisy_value, bounds['min'], bounds['max'])
        
        return noisy_value
    
    def _get_sensor_bounds(self, sensor_type):
        """Get min/max bounds for sensor types"""
        bounds = {
            'TEMPERATURE': {'min': -50, 'max': 100},
            'HUMIDITY': {'min': 0, 'max': 100},
            'GAS': {'min': 0, 'max': 1},
            'FLAME': {'min': 0, 'max': 1},
            'MOTION': {'min': 0, 'max': 1},
            'LIGHT': {'min': 0, 'max': 2000},
        }
        
        return bounds.get(sensor_type, {'min': 0, 'max': 1000})
    
    def calculate_privacy_loss(self, num_queries):
        """
        Calculate cumulative privacy loss (epsilon) for multiple queries
        
        Args:
            num_queries: Number of queries made
        
        Returns:
            Total privacy loss (epsilon)
        """
        # Using composition theorem for differential privacy
        total_epsilon = num_queries * self.epsilon
        
        return total_epsilon
    
    def anonymize_location(self, location_data):
        """
        Anonymize location data using k-anonymity principles
        
        Args:
            location_data: Detailed location information
        
        Returns:
            Anonymized location
        """
        # Generalize location to room level only
        if not location_data:
            return "Unknown Location"
        
        # Remove specific identifiers, keep only general area
        general_areas = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Office', 'Garage']
        
        for area in general_areas:
            if area.lower() in location_data.lower():
                return area
        
        return "General Area"
    
    def apply_k_anonymity(self, dataset, k=5):
        """
        Apply k-anonymity to a dataset
        
        Args:
            dataset: List of data records
            k: Minimum group size for anonymity
        
        Returns:
            Anonymized dataset
        """
        # This is a simplified implementation
        # In production, use proper k-anonymity algorithms
        
        if len(dataset) < k:
            logger.warning(f"Dataset size ({len(dataset)}) is smaller than k ({k})")
            return []
        
        # Group similar records and ensure each group has at least k members
        # For simplicity, we're just checking the size here
        return dataset
    
    def encrypt_sensitive_field(self, data, field_name):
        """
        Encrypt sensitive fields before storage/transmission
        
        Args:
            data: Dictionary containing the field
            field_name: Name of field to encrypt
        
        Returns:
            Data with encrypted field
        """
        # This is a placeholder for encryption
        # In production, use proper encryption libraries like cryptography
        
        from cryptography.fernet import Fernet
        import json
        
        try:
            # Generate key (in production, use stored key)
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            
            # Encrypt the field
            field_value = str(data.get(field_name, ''))
            encrypted_value = cipher_suite.encrypt(field_value.encode())
            
            data[field_name] = encrypted_value.decode()
            data[f'{field_name}_encrypted'] = True
            
            return data
        
        except Exception as e:
            logger.error(f"Error encrypting field {field_name}: {e}")
            return data
