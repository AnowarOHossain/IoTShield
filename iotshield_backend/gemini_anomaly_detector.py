"""
Gemini-Based Anomaly Detection for IoTShield
Uses Google Gemini API to analyze sensor data and detect anomalies
"""
import json
import logging
import asyncio
from typing import Dict, Tuple
import google.generativeai as genai
from django.conf import settings
from asgiref.sync import sync_to_async

logger = logging.getLogger('iotshield')


class GeminiAnomalyDetector:
    """Anomaly Detection using Gemini API"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            logger.info("Gemini Anomaly Detector initialized")
        else:
            logger.error("Gemini API key not configured!")
            self.model = None
    
    def analyze_with_gemini(self, sensor_data: Dict) -> Dict:
        """
        Call Gemini API to analyze IoT sensor data and detect anomalies.
        
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
            if not self.model:
                return self._fallback_analysis(sensor_data)
            
            # Create analysis prompt
            prompt = self._create_analysis_prompt(sensor_data)
            
            # Call Gemini API with timeout
            response = self._call_gemini_with_timeout(prompt, timeout=10)
            
            if response:
                # Parse JSON response
                result = self._parse_gemini_response(response)
                logger.info(f"Gemini analysis complete: anomaly={result['anomaly']}")
                return result
            else:
                logger.warning("Gemini API call timed out, using fallback")
                return self._fallback_analysis(sensor_data)
        
        except Exception as e:
            logger.error(f"Error in Gemini analysis: {e}")
            return self._fallback_analysis(sensor_data)
    
    async def analyze_with_gemini_async(self, sensor_data: Dict) -> Dict:
        """
        Async version of analyze_with_gemini for non-blocking operation
        """
        try:
            if not self.model:
                return self._fallback_analysis(sensor_data)
            
            # Create analysis prompt
            prompt = self._create_analysis_prompt(sensor_data)
            
            # Call Gemini API asynchronously
            response = await self._call_gemini_async(prompt)
            
            if response:
                result = self._parse_gemini_response(response)
                logger.info(f"Async Gemini analysis complete: anomaly={result['anomaly']}")
                return result
            else:
                return self._fallback_analysis(sensor_data)
        
        except Exception as e:
            logger.error(f"Error in async Gemini analysis: {e}")
            return self._fallback_analysis(sensor_data)
    
    def _create_analysis_prompt(self, sensor_data: Dict) -> str:
        """Create detailed prompt for Gemini analysis"""
        sensor_type = sensor_data.get('sensor_type', 'Unknown')
        value = sensor_data.get('value', 0)
        unit = sensor_data.get('unit', '')
        device_name = sensor_data.get('device_name', 'Unknown Device')
        location = sensor_data.get('location', 'Unknown Location')
        timestamp = sensor_data.get('timestamp', 'Unknown')
        
        # Get normal ranges for context
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

**Task:**
Determine if this sensor reading is normal or anomalous. Consider:
1. Is the value within expected range for this sensor type?
2. Could this indicate a safety hazard or system malfunction?
3. Does this require immediate attention?

**Required Response Format (JSON only, no markdown):**
{{
    "anomaly": true/false,
    "explanation": "Clear explanation of why this is or isn't an anomaly (2-3 sentences)",
    "severity": "LOW/MEDIUM/HIGH/CRITICAL",
    "suggestion": "Specific action recommendation (1-2 sentences)"
}}

Respond ONLY with valid JSON. No additional text or formatting.
"""
        return prompt
    
    def _get_normal_ranges(self, sensor_type: str) -> str:
        """Get normal ranges for different sensor types"""
        ranges = {
            'TEMPERATURE': 'Normal: 15-30°C, Warning: 30-40°C, Critical: >40°C or <0°C',
            'HUMIDITY': 'Normal: 30-60%, Warning: 60-80%, Critical: >80% or <20%',
            'GAS': 'Normal: 0-0.3, Warning: 0.3-0.6, Critical: >0.6 (potential gas leak)',
            'FLAME': 'Normal: 0-0.2, Warning: 0.2-0.5, Critical: >0.5 (fire hazard)',
            'MOTION': 'Normal: Expected motion patterns during active hours, Critical: Unexpected motion during off-hours',
            'LIGHT': 'Normal: Varies by time of day and location, typical indoor 100-500 lux',
        }
        return ranges.get(sensor_type, 'No predefined range available. Use expert judgment.')
    
    def _call_gemini_with_timeout(self, prompt: str, timeout: int = 10) -> str:
        """Call Gemini API with timeout"""
        try:
            # Use asyncio to add timeout
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def call_with_timeout():
                try:
                    response = await asyncio.wait_for(
                        self._call_gemini_async(prompt),
                        timeout=timeout
                    )
                    return response
                except asyncio.TimeoutError:
                    logger.warning(f"Gemini API call timed out after {timeout}s")
                    return None
            
            result = loop.run_until_complete(call_with_timeout())
            loop.close()
            return result
        
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return None
    
    async def _call_gemini_async(self, prompt: str) -> str:
        """Async call to Gemini API"""
        try:
            # Wrap sync API call in async
            response = await sync_to_async(self.model.generate_content)(prompt)
            return response.text if response else None
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return None
    
    def _parse_gemini_response(self, response_text: str) -> Dict:
        """Parse Gemini JSON response"""
        try:
            # Clean response (remove markdown code blocks if present)
            cleaned = response_text.strip()
            if cleaned.startswith('```'):
                # Remove markdown code block formatting
                lines = cleaned.split('\n')
                cleaned = '\n'.join(lines[1:-1] if len(lines) > 2 else lines)
            
            # Parse JSON
            result = json.loads(cleaned)
            
            # Validate required fields
            required_fields = ['anomaly', 'explanation', 'severity', 'suggestion']
            for field in required_fields:
                if field not in result:
                    logger.warning(f"Missing field '{field}' in Gemini response")
                    result[field] = self._get_default_value(field)
            
            return result
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini JSON response: {e}")
            logger.debug(f"Response text: {response_text}")
            return {
                'anomaly': False,
                'explanation': 'Unable to parse AI response',
                'severity': 'LOW',
                'suggestion': 'Manual review recommended'
            }
    
    def _get_default_value(self, field: str):
        """Get default value for missing fields"""
        defaults = {
            'anomaly': False,
            'explanation': 'Analysis incomplete',
            'severity': 'LOW',
            'suggestion': 'Review sensor data manually'
        }
        return defaults.get(field, '')
    
    def _fallback_analysis(self, sensor_data: Dict) -> Dict:
        """
        Fallback analysis when Gemini API is unavailable
        Uses rule-based thresholds
        """
        sensor_type = sensor_data.get('sensor_type', 'Unknown')
        value = sensor_data.get('value', 0)
        
        # Get threshold rules
        thresholds = self._get_threshold_rules(sensor_type)
        
        # Check against thresholds
        if value > thresholds.get('critical', float('inf')):
            return {
                'anomaly': True,
                'explanation': f'{sensor_type} value {value} exceeds critical threshold ({thresholds["critical"]}). Immediate attention required.',
                'severity': 'CRITICAL',
                'suggestion': f'Check {sensor_type.lower()} sensor and investigate cause immediately.'
            }
        elif value > thresholds.get('warning', float('inf')):
            return {
                'anomaly': True,
                'explanation': f'{sensor_type} value {value} is above warning threshold ({thresholds["warning"]}). Monitor closely.',
                'severity': 'HIGH',
                'suggestion': f'Monitor {sensor_type.lower()} trends and prepare for intervention if needed.'
            }
        elif value < thresholds.get('min', float('-inf')):
            return {
                'anomaly': True,
                'explanation': f'{sensor_type} value {value} is below minimum threshold ({thresholds["min"]}). Possible sensor malfunction.',
                'severity': 'MEDIUM',
                'suggestion': 'Check sensor connectivity and calibration.'
            }
        else:
            return {
                'anomaly': False,
                'explanation': f'{sensor_type} value {value} is within normal operating range.',
                'severity': 'LOW',
                'suggestion': 'No action required. Continue monitoring.'
            }
    
    def _get_threshold_rules(self, sensor_type: str) -> Dict:
        """Get threshold rules for rule-based fallback"""
        rules = {
            'TEMPERATURE': {'min': -5, 'warning': 35, 'critical': 45},
            'HUMIDITY': {'min': 10, 'warning': 70, 'critical': 85},
            'GAS': {'min': 0, 'warning': 0.4, 'critical': 0.6},
            'FLAME': {'min': 0, 'warning': 0.3, 'critical': 0.6},
            'MOTION': {'min': 0, 'warning': 0.8, 'critical': 1.0},
            'LIGHT': {'min': 0, 'warning': 800, 'critical': 1000},
        }
        return rules.get(sensor_type, {'min': 0, 'warning': 80, 'critical': 95})
