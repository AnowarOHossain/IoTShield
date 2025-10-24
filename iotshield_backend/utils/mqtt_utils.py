"""MQTT utility functions"""

import json
import logging

logger = logging.getLogger('iotshield')


def validate_mqtt_message(payload):
    """Validate MQTT message format"""
    required_fields = ['device_id', 'sensor_type', 'value', 'timestamp']
    
    try:
        data = json.loads(payload) if isinstance(payload, str) else payload
        
        for field in required_fields:
            if field not in data:
                logger.warning(f"Missing required field: {field}")
                return False
        
        return True
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON format in MQTT message")
        return False
    except Exception as e:
        logger.error(f"Error validating MQTT message: {e}")
        return False


def format_sensor_message(device_id, sensor_type, value, unit='', location=''):
    """Format sensor data for MQTT publishing"""
    from datetime import datetime
    
    message = {
        'device_id': device_id,
        'sensor_type': sensor_type,
        'value': value,
        'unit': unit,
        'location': location,
        'timestamp': datetime.now().isoformat()
    }
    
    return json.dumps(message)
