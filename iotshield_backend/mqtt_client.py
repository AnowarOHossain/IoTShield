"""
MQTT Client for IoTShield
Handles MQTT broker connection, subscription, and message processing
"""
import json
import logging
import paho.mqtt.client as mqtt
from django.conf import settings
from datetime import datetime

logger = logging.getLogger('iotshield')


class IoTShieldMQTTClient:
    """MQTT Client for IoTShield System"""
    
    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="iotshield_backend")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        # Set username and password if provided
        if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
        
        self.is_connected = False
    
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(
                settings.MQTT_BROKER_HOST,
                settings.MQTT_BROKER_PORT,
                settings.MQTT_KEEPALIVE
            )
            logger.info(f"Connecting to MQTT broker at {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}")
            self.client.loop_start()
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("Disconnected from MQTT broker")
    
    def on_connect(self, client, userdata, flags, reason_code, properties):
        """Callback when connected to broker"""
        if reason_code.is_failure:
            logger.error(f"Failed to connect to MQTT broker. Reason code: {reason_code}")
            self.is_connected = False
        else:
            self.is_connected = True
            logger.info("Successfully connected to MQTT broker")
            
            # Subscribe to topics
            topics = [
                (settings.MQTT_TOPIC_SENSORS, 0),
                (settings.MQTT_TOPIC_CONTROL, 0),
            ]
            
            for topic, qos in topics:
                client.subscribe(topic, qos)
                logger.info(f"Subscribed to topic: {topic}")
    
    def on_disconnect(self, client, userdata, flags, reason_code, properties):
        """Callback when disconnected from broker"""
        self.is_connected = False
        if reason_code is not None and reason_code.is_failure:
            logger.warning(f"Unexpected disconnection from MQTT broker. Reason code: {reason_code}")
        else:
            logger.info("Cleanly disconnected from MQTT broker")
    
    def on_message(self, client, userdata, msg):
        """Callback when message received"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            logger.debug(f"Received message on topic {topic}: {payload}")
            
            # Parse JSON payload
            data = json.loads(payload)
            
            # Route message based on topic
            if topic == settings.MQTT_TOPIC_SENSORS:
                self.handle_sensor_data(data)
            elif topic == settings.MQTT_TOPIC_CONTROL:
                self.handle_control_command(data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON message: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def handle_sensor_data(self, data):
        """Process incoming sensor data"""
        from .anomaly_detector import AnomalyDetector
        from .gemini_alerts import GeminiAlertGenerator
        from dashboard.models import Device, SensorData, Alert
        
        try:
            # Get or create device
            device, created = Device.objects.get_or_create(
                device_id=data.get('device_id'),
                defaults={
                    'device_type': data.get('device_type', 'ESP32'),
                    'name': data.get('device_name', f"Device {data.get('device_id')}"),
                    'location': data.get('location', ''),
                }
            )
            
            # Store sensor data
            sensor_data = SensorData.objects.create(
                device=device,
                sensor_type=data.get('sensor_type').upper(),
                value=float(data.get('value')),
                unit=data.get('unit', ''),
                timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat()))
            )
            
            # Check for anomalies
            detector = AnomalyDetector()
            is_anomaly, score = detector.detect_anomaly(sensor_data)
            
            if is_anomaly:
                sensor_data.is_anomaly = True
                sensor_data.anomaly_score = score
                sensor_data.save()
                
                # Generate AI alert
                alert_generator = GeminiAlertGenerator()
                alert_data = alert_generator.generate_alert(sensor_data, score)
                
                # Create alert
                alert = Alert.objects.create(
                    sensor_data=sensor_data,
                    title=alert_data.get('title'),
                    description=alert_data.get('description'),
                    ai_suggestion=alert_data.get('suggestion', ''),
                    severity=alert_data.get('severity', 'MEDIUM')
                )
                
                # Publish alert to MQTT
                self.publish_alert(alert)
                
                logger.info(f"Anomaly detected: {alert.title}")
            
        except Exception as e:
            logger.error(f"Error handling sensor data: {e}")
    
    def handle_control_command(self, data):
        """Process control command acknowledgment"""
        from .models import ControlCommand
        
        try:
            command_id = data.get('command_id')
            status = data.get('status')
            response = data.get('response', '')
            
            if command_id:
                command = ControlCommand.objects.get(id=command_id)
                command.status = status.upper()
                command.response = response
                if status.upper() == 'EXECUTED':
                    command.executed_at = datetime.now()
                command.save()
                
                logger.info(f"Control command {command_id} status updated: {status}")
        
        except ControlCommand.DoesNotExist:
            logger.warning(f"Control command {command_id} not found")
        except Exception as e:
            logger.error(f"Error handling control command: {e}")
    
    def publish(self, topic, payload, qos=0):
        """Publish message to MQTT topic"""
        if not self.is_connected:
            logger.warning("Not connected to MQTT broker. Cannot publish message.")
            return False
        
        try:
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            
            result = self.client.publish(topic, payload, qos)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Published message to {topic}")
                return True
            else:
                logger.error(f"Failed to publish message to {topic}")
                return False
        
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            return False
    
    def publish_alert(self, alert):
        """Publish alert to MQTT"""
        payload = {
            'alert_id': alert.id,
            'title': alert.title,
            'description': alert.description,
            'ai_suggestion': alert.ai_suggestion,
            'severity': alert.severity,
            'device_id': alert.sensor_data.device.device_id,
            'sensor_type': alert.sensor_data.sensor_type,
            'value': alert.sensor_data.value,
            'timestamp': alert.created_at.isoformat()
        }
        
        return self.publish(settings.MQTT_TOPIC_ALERTS, payload)
    
    def publish_control_command(self, command):
        """Publish control command to MQTT"""
        payload = {
            'command_id': command.id,
            'device_id': command.device.device_id,
            'command_type': command.command_type,
            'parameters': command.parameters,
            'timestamp': command.created_at.isoformat()
        }
        
        success = self.publish(settings.MQTT_TOPIC_CONTROL, payload)
        
        if success:
            command.status = 'SENT'
            command.save()
        
        return success


# Global MQTT client instance
mqtt_client = IoTShieldMQTTClient()
