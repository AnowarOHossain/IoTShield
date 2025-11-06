"""
Anomaly Detection Engine for IoTShield
Uses Isolation Forest for real-time anomaly detection
"""
import os
import logging
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger('iotshield')


class AnomalyDetector:
    """Anomaly Detection using Isolation Forest"""
    
    def __init__(self):
        self.model = None
        self.threshold = settings.ANOMALY_THRESHOLD
        self.load_model()
    
    def load_model(self):
        """Load pre-trained model or create new one"""
        try:
            if os.path.exists(settings.MODEL_PATH):
                self.model = joblib.load(settings.MODEL_PATH)
                logger.info(f"Loaded anomaly detection model from {settings.MODEL_PATH}")
            else:
                # Create new model with default parameters
                self.model = IsolationForest(
                    contamination=0.1,
                    random_state=42,
                    n_estimators=100
                )
                logger.info("Created new Isolation Forest model")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            # Fallback to new model
            self.model = IsolationForest(
                contamination=0.1,
                random_state=42,
                n_estimators=100
            )
    
    def save_model(self):
        """Save trained model to disk"""
        try:
            os.makedirs(os.path.dirname(settings.MODEL_PATH), exist_ok=True)
            joblib.dump(self.model, settings.MODEL_PATH)
            logger.info(f"Saved model to {settings.MODEL_PATH}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def detect_anomaly(self, sensor_data):
        """
        Detect if sensor reading is anomalous
        Returns: (is_anomaly: bool, anomaly_score: float)
        """
        try:
            # Extract features
            features = self.extract_features(sensor_data)
            
            if features is None:
                return False, 0.0
            
            # Reshape for single prediction
            features_array = np.array(features).reshape(1, -1)
            
            # Get anomaly prediction and score
            prediction = self.model.predict(features_array)
            score = self.model.score_samples(features_array)
            
            # Convert score to 0-1 range (more negative = more anomalous)
            normalized_score = self._normalize_score(score[0])
            
            # Prediction: -1 for anomaly, 1 for normal
            is_anomaly = prediction[0] == -1 or normalized_score > self.threshold
            
            return is_anomaly, normalized_score
        
        except Exception as e:
            logger.error(f"Error detecting anomaly: {e}")
            return False, 0.0
    
    def extract_features(self, sensor_data):
        """Extract features from sensor data for anomaly detection"""
        try:
            # Import here to avoid circular import
            from dashboard.models import SensorData
            
            # Get historical data for the same sensor type
            historical_data = SensorData.objects.filter(
                device=sensor_data.device,
                sensor_type=sensor_data.sensor_type,
                timestamp__gte=timezone.now() - timedelta(hours=1)
            ).order_by('-timestamp')[:100]
            
            if not historical_data.exists():
                return None
            
            # Extract statistical features
            values = [data.value for data in historical_data]
            
            features = [
                sensor_data.value,  # Current value
                np.mean(values),  # Mean of recent values
                np.std(values),  # Standard deviation
                np.max(values),  # Maximum value
                np.min(values),  # Minimum value
                sensor_data.value - np.mean(values),  # Deviation from mean
            ]
            
            return features
        
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return None
    
    def _normalize_score(self, score):
        """Normalize anomaly score to 0-1 range"""
        # Isolation Forest scores are typically between -0.5 and 0.5
        # More negative = more anomalous
        # Transform to 0-1 where 1 is most anomalous
        normalized = max(0, min(1, (-score + 0.5)))
        return normalized
    
    def train_model(self, training_data):
        """
        Train the anomaly detection model on historical data
        training_data: numpy array of shape (n_samples, n_features)
        """
        try:
            logger.info(f"Training model with {len(training_data)} samples...")
            self.model.fit(training_data)
            self.save_model()
            logger.info("Model training completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return False
    
    def get_sensor_thresholds(self, sensor_type):
        """Get predefined thresholds for different sensor types"""
        thresholds = {
            'TEMPERATURE': {'min': -10, 'low_warn': 5, 'medium_warn': 35, 'max': 50, 'critical': 45},
            'HUMIDITY': {'min': 0, 'low_warn': 15, 'medium_warn': 70, 'max': 100, 'critical': 90},
            'GAS': {'min': 0, 'low_warn': 0.1, 'medium_warn': 0.35, 'max': 1, 'critical': 0.6},
            'FLAME': {'min': 0, 'low_warn': 0.1, 'medium_warn': 0.4, 'max': 1, 'critical': 0.8},
            'MOTION': {'min': 0, 'low_warn': 0.3, 'medium_warn': 0.6, 'max': 1, 'critical': 1},
            'LIGHT': {'min': 0, 'low_warn': 50, 'medium_warn': 700, 'max': 1000, 'critical': 900},
        }
        
        return thresholds.get(sensor_type, {'min': 0, 'low_warn': 20, 'medium_warn': 70, 'max': 100, 'critical': 80})
    
    def check_threshold_violation(self, sensor_data):
        """Check if sensor value exceeds predefined thresholds"""
        thresholds = self.get_sensor_thresholds(sensor_data.sensor_type)
        
        # Check critical threshold first (highest priority)
        if sensor_data.value > thresholds['critical']:
            return True, 'CRITICAL', f"Value above critical threshold ({thresholds['critical']})"
        
        # Check HIGH threshold (above max but below critical)
        elif sensor_data.value > thresholds['max']:
            return True, 'HIGH', f"Value above maximum threshold ({thresholds['max']})"
        
        # Check MEDIUM threshold (approaching max, needs monitoring)
        elif sensor_data.value > thresholds['medium_warn']:
            return True, 'MEDIUM', f"Value approaching warning threshold ({thresholds['medium_warn']})"
        
        # Check LOW threshold (below minimum, possible sensor issue)
        elif sensor_data.value < thresholds['min']:
            return True, 'LOW', f"Value below minimum threshold ({thresholds['min']})"
        
        # Check LOW severity for slightly below normal
        elif sensor_data.value < thresholds['low_warn']:
            return True, 'LOW', f"Value below normal range ({thresholds['low_warn']})"
        
        return False, 'NORMAL', "Value within normal range"
