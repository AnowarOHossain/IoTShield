"""
Gemini AI Alert Generator for IoTShield
Generates human-readable alerts using Google's Gemini API
"""
import logging
import google.generativeai as genai
from django.conf import settings

logger = logging.getLogger('iotshield')


class GeminiAlertGenerator:
    """Generate intelligent alerts using Gemini API"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            logger.warning("Gemini API key not configured. AI alerts will not be generated.")
            self.model = None
    
    def generate_alert(self, sensor_data, anomaly_score):
        """
        Generate a human-readable alert for anomalous sensor data
        Returns dict with title, description, suggestion, and severity
        """
        try:
            if not self.model:
                return self._fallback_alert(sensor_data, anomaly_score)
            
            # Create context for Gemini
            context = self._create_context(sensor_data, anomaly_score)
            
            # Generate alert using Gemini
            prompt = f"""
You are an IoT security system assistant. Analyze the following sensor anomaly and generate a brief, actionable alert.

Context:
{context}

Provide a JSON response with the following fields:
- title: A short, clear alert title (max 10 words)
- description: A brief description of the anomaly (2-3 sentences)
- suggestion: Specific action recommendation (1-2 sentences)
- severity: One of [LOW, MEDIUM, HIGH, CRITICAL]

Format the response as valid JSON only, without any markdown formatting or code blocks.
"""
            
            response = self.model.generate_content(prompt)
            
            # Parse response
            import json
            alert_data = json.loads(response.text.strip())
            
            logger.info(f"Generated Gemini alert for {sensor_data.sensor_type}")
            return alert_data
        
        except Exception as e:
            logger.error(f"Error generating Gemini alert: {e}")
            return self._fallback_alert(sensor_data, anomaly_score)
    
    def _create_context(self, sensor_data, anomaly_score):
        """Create context string for Gemini"""
        context = f"""
Sensor Type: {sensor_data.sensor_type}
Current Value: {sensor_data.value} {sensor_data.unit}
Anomaly Score: {anomaly_score:.2f} (0=normal, 1=highly anomalous)
Device: {sensor_data.device.name}
Location: {sensor_data.device.location or 'Unknown'}
Timestamp: {sensor_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
"""
        return context.strip()
    
    def _fallback_alert(self, sensor_data, anomaly_score):
        """Generate fallback alert when Gemini API is unavailable"""
        sensor_type = sensor_data.sensor_type
        value = sensor_data.value
        unit = sensor_data.unit
        location = sensor_data.device.location or sensor_data.device.name
        
        # Determine severity based on anomaly score
        if anomaly_score >= 0.9:
            severity = 'CRITICAL'
        elif anomaly_score >= 0.7:
            severity = 'HIGH'
        elif anomaly_score >= 0.5:
            severity = 'MEDIUM'
        else:
            severity = 'LOW'
        
        # Generate sensor-specific alerts
        alerts = {
            'TEMPERATURE': {
                'title': f'Abnormal Temperature Detected: {value}{unit}',
                'description': f'Temperature reading of {value}{unit} detected in {location}. This is significantly different from normal patterns.',
                'suggestion': 'Check HVAC system and ensure proper ventilation. Monitor temperature trends.',
            },
            'HUMIDITY': {
                'title': f'Unusual Humidity Level: {value}{unit}',
                'description': f'Humidity level of {value}{unit} detected in {location}. This deviates from expected range.',
                'suggestion': 'Verify dehumidifier/humidifier settings. Check for water leaks or condensation.',
            },
            'GAS': {
                'title': f'Gas Leak Detected: {value}{unit}',
                'description': f'Potentially dangerous gas levels ({value}{unit}) detected in {location}. Immediate attention required.',
                'suggestion': 'Evacuate area immediately. Turn off gas supply. Ventilate the space and contact emergency services if necessary.',
            },
            'FLAME': {
                'title': f'Fire Hazard Alert: {value}{unit}',
                'description': f'Flame or extreme heat detected in {location} with reading of {value}{unit}.',
                'suggestion': 'Investigate immediately. Prepare fire extinguisher. Evacuate if fire is confirmed and call emergency services.',
            },
            'MOTION': {
                'title': f'Unexpected Motion Detected',
                'description': f'Unusual motion activity detected in {location} at an unexpected time.',
                'suggestion': 'Review security cameras. Verify if authorized personnel are present. Consider security alert.',
            },
            'LIGHT': {
                'title': f'Abnormal Light Level: {value}{unit}',
                'description': f'Unusual lighting conditions detected in {location} with reading of {value}{unit}.',
                'suggestion': 'Check lighting system. Verify scheduled lighting patterns. Inspect for equipment malfunction.',
            },
        }
        
        alert_template = alerts.get(sensor_type, {
            'title': f'Anomaly Detected: {sensor_type}',
            'description': f'Unusual {sensor_type.lower()} reading of {value}{unit} detected in {location}.',
            'suggestion': 'Investigate the sensor and surrounding area. Verify system functionality.',
        })
        
        return {
            'title': alert_template['title'],
            'description': alert_template['description'],
            'suggestion': alert_template['suggestion'],
            'severity': severity
        }
    
    def generate_summary(self, alerts_list):
        """Generate a summary of multiple alerts"""
        if not self.model or not alerts_list:
            return "Multiple anomalies detected. Review individual alerts for details."
        
        try:
            # Create summary prompt
            alert_descriptions = "\n".join([
                f"- [{alert.severity}] {alert.title}"
                for alert in alerts_list[:10]  # Limit to 10 most recent
            ])
            
            prompt = f"""
Provide a brief executive summary (2-3 sentences) of the following IoT security alerts:

{alert_descriptions}

Focus on the most critical issues and overall system health.
"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        
        except Exception as e:
            logger.error(f"Error generating alert summary: {e}")
            return "Multiple anomalies detected. Review individual alerts for details."
