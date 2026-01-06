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
{{
    "anomaly": true/false,
    "explanation": "Clear explanation of why this is or isn't an anomaly, including deviation percentage if relevant (2-3 sentences)",
    "severity": "LOW/MEDIUM/HIGH/CRITICAL",
    "suggestion": "Specific action recommendation appropriate to severity level (1-2 sentences)"
}}

Respond ONLY with valid JSON. No additional text or formatting.
"""
        return prompt
    
    def _get_normal_ranges(self, sensor_type: str) -> str:
        """Get normal ranges for different sensor types"""
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
        
        # Check against thresholds (multi-level severity)
        if value > thresholds.get('critical', float('inf')) or value < thresholds.get('min', float('-inf')):
            return {
                'anomaly': True,
                'explanation': f'{sensor_type} value {value} exceeds critical threshold. Extreme deviation detected, immediate attention required.',
                'severity': 'CRITICAL',
                'suggestion': f'Immediately check {sensor_type.lower()} sensor and investigate cause. Take safety precautions.'
            }
        elif value > thresholds.get('high', float('inf')):
            return {
                'anomaly': True,
                'explanation': f'{sensor_type} value {value} significantly exceeds high threshold ({thresholds["high"]}). Requires investigation.',
                'severity': 'HIGH',
                'suggestion': f'Investigate {sensor_type.lower()} readings and prepare for intervention if trend continues.'
            }
        elif value > thresholds.get('medium', float('inf')):
            return {
                'anomaly': True,
                'explanation': f'{sensor_type} value {value} exceeds medium threshold ({thresholds["medium"]}). Notable deviation from normal.',
                'severity': 'MEDIUM',
                'suggestion': f'Monitor {sensor_type.lower()} closely. Check if pattern persists over next readings.'
            }
        elif value > thresholds.get('low', float('inf')):
            return {
                'anomaly': True,
                'explanation': f'{sensor_type} value {value} slightly exceeds normal range. Minor deviation detected.',
                'severity': 'LOW',
                'suggestion': f'Keep monitoring {sensor_type.lower()}. No immediate action needed unless trend worsens.'
            }
        else:
            return {
                'anomaly': False,
                'explanation': f'{sensor_type} value {value} is within normal operating range.',
                'severity': 'LOW',
                'suggestion': 'No action required. Continue routine monitoring.'
            }
    
    def _get_threshold_rules(self, sensor_type: str) -> Dict:
        """Get threshold rules for rule-based fallback"""
        rules = {
            'TEMPERATURE': {'min': 0, 'low': 32, 'medium': 38, 'high': 45, 'critical': 50},
            'HUMIDITY': {'min': 15, 'low': 65, 'medium': 75, 'high': 85, 'critical': 90},
            'GAS': {'min': 0, 'low': 0.36, 'medium': 0.51, 'high': 0.66, 'critical': 0.76},
            'FLAME': {'min': 0, 'low': 0.16, 'medium': 0.36, 'high': 0.56, 'critical': 0.71},
            'MOTION': {'min': 0, 'low': 0.4, 'medium': 0.6, 'high': 0.75, 'critical': 0.90},
            'LIGHT': {'min': 20, 'low': 650, 'medium': 800, 'high': 900, 'critical': 950},
            'CPU_TEMPERATURE': {'min': 0, 'low': 70, 'medium': 80, 'high': 90, 'critical': 95},
            'MEMORY_USAGE': {'min': 0, 'low': 75, 'medium': 85, 'high': 92, 'critical': 95},
            'DISK_USAGE': {'min': 0, 'low': 75, 'medium': 85, 'high': 92, 'critical': 95},
        }
        return rules.get(sensor_type, {'min': 0, 'low': 70, 'medium': 80, 'high': 90, 'critical': 95})
