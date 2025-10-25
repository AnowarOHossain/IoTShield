"""MQTT Publisher for Simulator"""

import json
import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger('simulator')


class MQTTPublisher:
    """MQTT Publisher for sending sensor data"""
    
    def __init__(self, broker_host, broker_port, client_id):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        
        self.is_connected = False
    
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            logger.info(f"Connecting to MQTT broker at {self.broker_host}:{self.broker_port}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("Disconnected from MQTT broker")
    
    def on_connect(self, client, userdata, flags, reason_code, properties):
        """Callback when connected"""
        if reason_code.is_failure:
            logger.error(f"Failed to connect. Reason code: {reason_code}")
            self.is_connected = False
        else:
            self.is_connected = True
            logger.info("Successfully connected to MQTT broker")
    
    def on_disconnect(self, client, userdata, flags, reason_code, properties):
        """Callback when disconnected"""
        self.is_connected = False
        if reason_code is not None and reason_code.is_failure:
            logger.warning(f"Unexpected disconnection. Reason code: {reason_code}")
    
    def on_publish(self, client, userdata, mid, reason_code, properties):
        """Callback when message published"""
        logger.debug(f"Message {mid} published")
    
    def publish(self, topic, message):
        """Publish message to topic"""
        if not self.is_connected:
            logger.warning("Not connected to broker. Cannot publish.")
            return False
        
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            
            result = self.client.publish(topic, message, qos=0)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                return True
            else:
                logger.error(f"Failed to publish message. Return code: {result.rc}")
                return False
        
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            return False
