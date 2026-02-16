"""
Ollama-Based Anomaly Detection for IoTShield
Uses Ollama API with llama3.2:1b model to analyze sensor data and detect anomalies
This replaces TinyLlama transformers for better performance and easier deployment
"""
import json
import logging
import requests
from typing import Dict
from django.conf import settings

logger = logging.getLogger('iotshield')


class OllamaAnomalyDetector:
    """Anomaly Detection using Ollama with llama3.2:1b model"""
    
    def __init__(self):
        """Initialize Ollama detector with llama3.2:1b model"""
        self.ollama_host = getattr(settings, 'OLLAMA_HOST', 'http://localhost:11434')
        self.model_name = getattr(settings, 'OLLAMA_MODEL', 'llama3.2:1b')
        self.api_endpoint = f"{self.ollama_host}/api/generate"
        
        logger.info(f"Ollama Anomaly Detector initialized with model: {self.model_name}")
    
    def analyze(self, sensor_data: Dict) -> Dict:
        """
        Analyze IoT sensor data and detect anomalies using Ollama.
        Args:
            sensor_data: Dictionary containing sensor information
        Returns:
            Dictionary with fields:
            - anomaly (bool): Whether the data is anomalous
            - explanation (str): Explanation of the analysis
            - severity (str): Severity level [LOW, MEDIUM, HIGH, CRITICAL]
            - suggestion (str): Recommended action
        """
        try:
            prompt = self._create_analysis_prompt(sensor_data)
            response = self._call_ollama_api(prompt)
            result = self._parse_ollama_response(response)
            logger.info(f"Ollama analysis complete: anomaly={result['anomaly']}")
            return result
        except Exception as e:
            logger.error(f"Error in Ollama analysis: {e}")
            return self._get_fallback_response(sensor_data)
    
    def _create_analysis_prompt(self, sensor_data: Dict) -> str:
        """Create analysis prompt for the LLM"""
        sensor_type = sensor_data.get('sensor_type', 'Unknown')
        value = sensor_data.get('value', 0)
        unit = sensor_data.get('unit', '')
        device_name = sensor_data.get('device_name', 'Unknown Device')
        location = sensor_data.get('location', 'Unknown Location')
        timestamp = sensor_data.get('timestamp', 'Unknown')
        normal_ranges = self._get_normal_ranges(sensor_type)
        
        prompt = f"""You are an IoT security and monitoring expert. Analyze the following sensor data and determine if it represents an anomaly or normal behavior.

**Sensor Data:**
- Sensor Type: {sensor_type}
- Current Value: {value} {unit}
- Device: {device_name}
- Location: {location}
- Timestamp: {timestamp}

**Normal Range Context:**
{normal_ranges}

**Severity Classification Guidelines:**
- **LOW**: Minor deviation from normal (5-15% outside normal range). Informational only, no immediate action needed.
- **MEDIUM**: Moderate deviation (15-30% outside normal range). Monitor closely, may need attention soon.
- **HIGH**: Significant deviation (30-50% outside normal range) or approaching danger threshold. Requires investigation.
- **CRITICAL**: Extreme deviation (>50% outside normal range) or exceeds safety threshold. Immediate action required, potential danger.

**Examples:**
- Temperature 32°C (normal: 20-28°C) → MEDIUM (slightly warm, monitor)
- Temperature 38°C (normal: 20-28°C) → HIGH (uncomfortably hot, investigate)
- Temperature 48°C (normal: 20-28°C) → CRITICAL (dangerous heat, immediate action)
- Humidity 65% (normal: 30-60%) → LOW (slightly high, informational)
- Gas 0.35 ppm (normal: 0-0.3) → MEDIUM (elevated, monitor for leak)
- Gas 0.75 ppm (critical: >0.7) → CRITICAL (dangerous leak, evacuate)

**Task:**
Determine if this sensor reading is normal or anomalous. Consider:
1. Is the value within expected range for this sensor type?
2. How far is it from the normal range (percentage deviation)?
3. Does it pose an immediate safety risk?
4. Use LOW/MEDIUM for minor deviations, reserve HIGH/CRITICAL for genuine concerns.

**Required Response Format (JSON only, no markdown):**
{{"anomaly": true or false, "explanation": "Clear explanation of why this is or isn't an anomaly, including deviation percentage if relevant (2-3 sentences)", "severity": "LOW or MEDIUM or HIGH or CRITICAL", "suggestion": "Specific action recommendation appropriate to severity level (1-2 sentences)"}}

Respond ONLY with valid JSON. No additional text or formatting.
"""
        return prompt
    
    def _get_normal_ranges(self, sensor_type: str) -> str:
        """Get normal ranges for sensor types"""
        ranges = {
            'TEMPERATURE': 'Normal: 18-28°C, Low Alert: 28-35°C or 10-18°C, Medium Alert: 35-42°C or 5-10°C, High Alert: 42-50°C or 0-5°C, Critical: >50°C or <0°C',
            'HUMIDITY': 'Normal: 30-60%, Low Alert: 60-70% or 20-30%, Medium Alert: 70-80% or 15-20%, High Alert: 80-90% or 10-15%, Critical: >90% or <10%',
            'GAS': 'Normal: 0-0.35 ppm, Low Alert: 0.36-0.50 ppm, Medium Alert: 0.51-0.65 ppm, High Alert: 0.66-0.75 ppm, Critical: >0.76 ppm (dangerous leak)',
            'FLAME': 'Normal: 0-0.15, Low Alert: 0.16-0.35, Medium Alert: 0.36-0.55, High Alert: 0.56-0.70, Critical: >0.71 (fire detected)',
            'MOTION': 'Normal: 0-0.4 (low activity), Low Alert: 0.4-0.6 (moderate activity), Medium Alert: 0.6-0.75 (high activity), High Alert: 0.75-0.90 (unusual), Critical: >0.90 (suspicious)',
            'LIGHT': 'Normal: 100-600 lux (indoor), Low Alert: 600-800 lux, Medium Alert: 800-900 lux or <50 lux, High Alert: >900 lux or <20 lux',
            'CPU_TEMPERATURE': 'Normal: 30-65°C, Low Alert: 65-75°C, Medium Alert: 75-85°C, High Alert: 85-95°C, Critical: >95°C',
            'MEMORY_USAGE': 'Normal: 0-70%, Low Alert: 70-80%, Medium Alert: 80-90%, High Alert: 90-95%, Critical: >95%',
            'DISK_USAGE': 'Normal: 0-70%, Low Alert: 70-80%, Medium Alert: 80-90%, High Alert: 90-95%, Critical: >95%',
        }
        return ranges.get(sensor_type, 'No predefined range available. Use expert judgment and classify based on reasonable deviation from expected values.')
    
    def _call_ollama_api(self, prompt: str) -> str:
        """Call Ollama API to generate response"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40
            }
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                raise Exception(f"Ollama API returned status code {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            logger.error(f"Failed to connect to Ollama at {self.ollama_host}. Is Ollama running?")
            raise Exception(f"Cannot connect to Ollama at {self.ollama_host}")
        except requests.exceptions.Timeout:
            logger.error("Ollama API request timeout")
            raise Exception("Ollama API request timeout")
        except Exception as e:
            logger.error(f"Error calling Ollama API: {e}")
            raise
    
    def _parse_ollama_response(self, response_text: str) -> Dict:
        """Parse JSON response from Ollama"""
        try:
            # Clean up response
            cleaned = response_text.strip()
            
            # Remove markdown code blocks if present
            if '```json' in cleaned:
                start = cleaned.find('{')
                end = cleaned.rfind('}') + 1
                if start >= 0 and end > start:
                    cleaned = cleaned[start:end]
            elif '```' in cleaned:
                lines = cleaned.split('\n')
                cleaned = '\n'.join(lines[1:-1] if len(lines) > 2 else lines)
            
            # Try to find JSON object in response
            if '{' in cleaned:
                start = cleaned.find('{')
                end = cleaned.rfind('}') + 1
                if start >= 0 and end > start:
                    cleaned = cleaned[start:end]
            
            result = json.loads(cleaned)
            
            # Validate required fields
            required_fields = ['anomaly', 'explanation', 'severity', 'suggestion']
            for field in required_fields:
                if field not in result:
                    result[field] = self._get_default_value(field)
            
            # Ensure anomaly is boolean
            if isinstance(result['anomaly'], str):
                result['anomaly'] = result['anomaly'].lower() in ['true', '1', 'yes']
            
            # Validate severity
            valid_severities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
            if result['severity'] not in valid_severities:
                result['severity'] = 'LOW'
            
            return result
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Ollama JSON response: {e}")
            logger.debug(f"Response was: {response_text}")
            return self._get_default_response()
        except Exception as e:
            logger.error(f"Error parsing Ollama response: {e}")
            return self._get_default_response()
    
    def _get_default_value(self, field: str):
        """Get default value for a field"""
        defaults = {
            'anomaly': False,
            'explanation': 'Analysis incomplete',
            'severity': 'LOW',
            'suggestion': 'Review sensor data manually'
        }
        return defaults.get(field, '')
    
    def _get_default_response(self) -> Dict:
        """Get default response when parsing fails"""
        return {
            'anomaly': False,
            'explanation': 'Unable to analyze - check Ollama connection',
            'severity': 'LOW',
            'suggestion': 'Manual review recommended'
        }
    
    def _get_fallback_response(self, sensor_data: Dict) -> Dict:
        """Get fallback response based on simple rules when Ollama fails"""
        logger.warning("Using fallback analysis - Ollama unavailable")
        
        sensor_type = sensor_data.get('sensor_type', '')
        value = float(sensor_data.get('value', 0))
        
        # Simple rule-based fallback
        if sensor_type == 'TEMPERATURE':
            if value > 45 or value < 5:
                return {
                    'anomaly': True,
                    'explanation': f'Temperature {value}°C is outside safe range',
                    'severity': 'CRITICAL' if value > 50 or value < 0 else 'HIGH',
                    'suggestion': 'Check heating/cooling system immediately'
                }
            elif value > 35 or value < 15:
                return {
                    'anomaly': True,
                    'explanation': f'Temperature {value}°C is above normal',
                    'severity': 'MEDIUM',
                    'suggestion': 'Monitor temperature closely'
                }
        
        elif sensor_type == 'GAS':
            if value > 0.7:
                return {
                    'anomaly': True,
                    'explanation': f'Gas level {value} ppm indicates possible leak',
                    'severity': 'CRITICAL',
                    'suggestion': 'Evacuate area and check for gas leak'
                }
            elif value > 0.35:
                return {
                    'anomaly': True,
                    'explanation': f'Gas level {value} ppm is elevated',
                    'severity': 'MEDIUM',
                    'suggestion': 'Monitor gas levels closely'
                }
        
        # Default: normal
        return {
            'anomaly': False,
            'explanation': 'Reading appears normal based on fallback analysis',
            'severity': 'LOW',
            'suggestion': 'Continue normal operation'
        }
