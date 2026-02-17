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
        
        # Initialize anomaly detector once (singleton pattern)
        from .ollama_anomaly_detector import OllamaAnomalyDetector
        self.anomaly_detector = OllamaAnomalyDetector()
    
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
        """This function runs whenever we receive an MQTT message"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            logger.debug(f"Received message on topic {topic}: {payload[:100]}...") 
            
            # Convert JSON string to Python dict
            data = json.loads(payload)
            
            # Here's the security layer - decrypt if message is encrypted
            # This protects us even if the MQTT broker is compromised
            from .privacy_engine import rsa_encryption
            if rsa_encryption:
                data = rsa_encryption.decrypt_mqtt_payload(data)
            
            # Now route the decrypted message to the right handler
            if topic == settings.MQTT_TOPIC_SENSORS:
                self.handle_sensor_data(data)       # Handle sensor readings
            elif topic == settings.MQTT_TOPIC_CONTROL:
                self.handle_control_command(data)   # Handle control commands
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON message: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def handle_sensor_data(self, data):
        """Process incoming sensor data"""
        from dashboard.models import Device, SensorData, Alert
        import threading
        
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
            
            # Analyze with Ollama API in background thread to avoid blocking
            def analyze_and_alert():
                try:
                    # Use the singleton detector instance
                    sensor_dict = {
                        'sensor_type': sensor_data.sensor_type,
                        'value': sensor_data.value,
                        'unit': sensor_data.unit,
                        'device_name': device.name,
                        'location': device.location,
                        'timestamp': sensor_data.timestamp.isoformat(),
                    }
                    
                    # Call Ollama API for anomaly analysis using singleton detector
                    analysis_result = self.anomaly_detector.analyze(sensor_dict)
                    
                    # Update sensor data with analysis results
                    sensor_data.is_anomaly = analysis_result.get('anomaly', False)
                    sensor_data.anomaly_score = 1.0 if analysis_result.get('anomaly') else 0.0
                    sensor_data.save()
                    
                    # Create alert if anomalous
                    if analysis_result.get('anomaly', False):
                        alert = Alert.objects.create(
                            sensor_data=sensor_data,
                            title=f"{sensor_data.sensor_type} Anomaly Detected",
                            description=analysis_result.get('explanation', 'Anomalous sensor reading detected'),
                            ai_suggestion=analysis_result.get('suggestion', ''),
                            severity=analysis_result.get('severity', 'MEDIUM')
                        )
                        
                        # Publish alert to MQTT
                        self.publish_alert(alert)
                        
                        logger.info(f"Anomaly detected by Ollama: {alert.title}")
                        
                        # Send email notification for CRITICAL/HIGH alerts
                        from iotshield_backend.utils.email_alerts import send_alert_email
                        
                        # Prepare email data
                        email_data = {
                            'device_name': device.name,
                            'severity': alert.severity,
                            'sensor_type': sensor_data.sensor_type,
                            'sensor_value': f"{sensor_data.value} {sensor_data.unit}",
                            'description': alert.description,
                            'timestamp': alert.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            'additional_data': {
                                'Device ID': device.device_id,
                                'Device Type': device.device_type,
                                'Location': device.location or 'Not specified',
                                'Sensor Type': sensor_data.sensor_type,
                                'Reading': f"{sensor_data.value} {sensor_data.unit}",
                                'AI Suggestion': alert.ai_suggestion or 'No suggestion available'
                            }
                        }
                        
                        # Send email asynchronously
                        email_thread = threading.Thread(target=send_alert_email, args=(email_data,), daemon=True)
                        email_thread.start()
                    else:
                        logger.debug(f"Normal reading: {sensor_data.sensor_type}={sensor_data.value}")
                
                except Exception as e:
                    logger.error(f"Error in anomaly analysis: {e}")
            
            # Run analysis in background thread
            analysis_thread = threading.Thread(target=analyze_and_alert, daemon=True)
            analysis_thread.start()
            
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
