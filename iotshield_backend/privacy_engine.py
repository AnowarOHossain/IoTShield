"""
Privacy-Preserving Engine for IoTShield
Implements differential privacy through noise addition and RSA encryption
"""
import logging
import numpy as np
import base64
import json
from pathlib import Path
from django.conf import settings
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

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


class RSAEncryption:
    """
    This class handles RSA encryption and decryption for securing MQTT messages.
    It protects sensor data even if someone compromises the MQTT broker.
    """
    
    def __init__(self, key_size=2048):
        """
        Set up the RSA encryption system.
        We use 2048-bit keys which provides strong security for IoT.
        """
        self.key_size = key_size
        # Private key is used for decryption - only gateway has this
        self.private_key = None
        # Public key is used for encryption - ESP32 devices will have this
        self.public_key = None
        # Cipher object for actual encryption/decryption operations
        self.cipher = None
        
        # Set up file paths where keys will be stored
        self.keys_dir = Path(settings.BASE_DIR) / 'keys'
        self.private_key_path = self.keys_dir / 'rsa_private.pem'  # Keep this secret!
        self.public_key_path = self.keys_dir / 'rsa_public.pem'    # Can share with devices
        
        # Automatically load or create keys when this class is initialized
        self._initialize_keys()
    
    def _initialize_keys(self):
        """Load keys from disk if they exist, otherwise create new ones"""
        try:
            # Make sure the keys folder exists
            self.keys_dir.mkdir(exist_ok=True)
            
            # Check if we already have keys saved
            if self.private_key_path.exists() and self.public_key_path.exists():
                # Keys found, load them from files
                self.load_keys()
                logger.info("RSA keys loaded successfully")
            else:
                # First time setup - generate new key pair
                logger.info("RSA keys not found. Generating new key pair...")
                self.generate_keys()
                logger.info("RSA keys generated and saved successfully")
        
        except Exception as e:
            logger.error(f"Error initializing RSA keys: {e}")
            raise
    
    def generate_keys(self):
        """Create a new public/private key pair using RSA algorithm"""
        try:
            # Use PyCryptodome to generate the keys
            key = RSA.generate(self.key_size)
            # Full key contains both public and private components
            self.private_key = key
            # Extract just the public key part to share with devices
            self.public_key = key.publickey()
            
            # Save both keys to disk for future use
            self.save_keys()
            
            # Set up the cipher object using OAEP padding (more secure than basic RSA)
            self.cipher = PKCS1_OAEP.new(self.private_key)
            
            logger.info(f"Generated {self.key_size}-bit RSA key pair")
            
        except Exception as e:
            logger.error(f"Error generating RSA keys: {e}")
            raise
    
    def save_keys(self):
        """Write the keys to files in PEM format"""
        try:
            # Write private key to file (must keep this secret!)
            with open(self.private_key_path, 'wb') as f:
                f.write(self.private_key.export_key('PEM'))
            
            # Write public key to separate file (this one we can share with ESP32)
            with open(self.public_key_path, 'wb') as f:
                f.write(self.public_key.export_key('PEM'))
            
            # Try to set file permissions so only owner can read private key
            # This works on Linux/Mac but not Windows
            try:
                import os
                os.chmod(self.private_key_path, 0o600)
            except Exception:
                pass  # Skip on Windows
            
            logger.info("RSA keys saved to disk")
            
        except Exception as e:
            logger.error(f"Error saving RSA keys: {e}")
            raise
    
    def load_keys(self):
        """Read existing keys from disk"""
        try:
            # Read the private key file
            with open(self.private_key_path, 'rb') as f:
                self.private_key = RSA.import_key(f.read())
            
            # Read the public key file
            with open(self.public_key_path, 'rb') as f:
                self.public_key = RSA.import_key(f.read())
            
            # Set up cipher for decryption using the private key
            self.cipher = PKCS1_OAEP.new(self.private_key)
            
            logger.debug("RSA keys loaded from disk")
            
        except Exception as e:
            logger.error(f"Error loading RSA keys: {e}")
            raise
    
    def get_public_key_pem(self):
        """
        Export public key as a string that can be copied to ESP32 firmware.
        This key is safe to share - it can only encrypt, not decrypt.
        """
        return self.public_key.export_key('PEM').decode('utf-8')
    
    def encrypt(self, data):
        """
        Encrypt data with public key. 
        In real deployment, ESP32 does this before sending to MQTT.
        We include it here for testing purposes.
        """
        try:
            # If data is a dict, convert it to JSON string first
            if isinstance(data, dict):
                data = json.dumps(data)
            
            # Convert string to bytes for encryption
            data_bytes = data.encode('utf-8')
            
            # RSA has size limits - can't encrypt huge data
            # Calculate max size based on key size and padding
            max_chunk_size = (self.key_size // 8) - 42  # OAEP padding takes 42 bytes
            
            if len(data_bytes) > max_chunk_size:
                raise ValueError(f"Data too large for RSA encryption. Max: {max_chunk_size} bytes")
            
            # Do the actual encryption using public key
            cipher_encrypt = PKCS1_OAEP.new(self.public_key)
            encrypted = cipher_encrypt.encrypt(data_bytes)
            
            # Convert binary data to base64 text for transmission over MQTT
            encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
            
            logger.debug(f"Data encrypted successfully ({len(data_bytes)} bytes)")
            
            return encrypted_b64
        
        except Exception as e:
            logger.error(f"Error encrypting data: {e}")
            raise
    
    def decrypt(self, encrypted_data):
        """
        Decrypt data that was encrypted with our public key.
        Only works if we have the matching private key.
        """
        try:
            # First, decode the base64 text back to binary
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            # Use private key to decrypt the data
            decrypted = self.cipher.decrypt(encrypted_bytes)
            
            # Convert decrypted bytes back to string
            decrypted_str = decrypted.decode('utf-8')
            
            # Try to parse as JSON (most sensor data is JSON)
            try:
                decrypted_data = json.loads(decrypted_str)
            except json.JSONDecodeError:
                # If not JSON, just return as plain string
                decrypted_data = decrypted_str
            
            logger.debug("Data decrypted successfully")
            
            return decrypted_data
        
        except Exception as e:
            logger.error(f"Error decrypting data: {e}")
            raise
    
    def encrypt_mqtt_payload(self, payload):
        """
        Wrap sensor data in encrypted format for MQTT.
        Creates a standardized encrypted message structure.
        """
        try:
            # Build the encrypted message with metadata
            # Gateway will know this is encrypted and how to decrypt it
            encrypted_payload = {
                'encrypted': True,                    # Flag to indicate encryption
                'encryption_type': 'RSA-OAEP',       # Algorithm used
                'key_size': self.key_size,           # Key strength
                'data': self.encrypt(payload)        # The actual encrypted data
            }
            
            return encrypted_payload
        
        except Exception as e:
            logger.error(f"Error encrypting MQTT payload: {e}")
            return payload  # Return original payload on error
    
    def decrypt_mqtt_payload(self, payload):
        """
        Unwrap and decrypt incoming MQTT messages from ESP32.
        If message is not encrypted, just pass it through unchanged.
        """
        try:
            # First check if this message is even encrypted
            if not isinstance(payload, dict) or not payload.get('encrypted'):
                # Not encrypted, return as-is (allows gradual migration)
                logger.debug("Payload is not encrypted, returning as-is")
                return payload
            
            # Make sure we support this encryption type
            if payload.get('encryption_type') != 'RSA-OAEP':
                logger.warning(f"Unsupported encryption type: {payload.get('encryption_type')}")
                return payload
            
            # Extract encrypted data and decrypt it
            encrypted_data = payload.get('data')
            decrypted_data = self.decrypt(encrypted_data)
            
            return decrypted_data
        
        except Exception as e:
            # If decryption fails, log error but don't crash the system
            logger.error(f"Error decrypting MQTT payload: {e}")
            return payload


# Create a single RSA encryption instance that the whole app can use
# If this fails (e.g., key generation error), set to None to allow app to run
try:
    rsa_encryption = RSAEncryption()
except Exception as e:
    logger.warning(f"Failed to initialize RSA encryption: {e}")
    rsa_encryption = None
