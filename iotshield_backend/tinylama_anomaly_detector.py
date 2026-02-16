"""
TinyLlama-Based Anomaly Detection for IoTShield
Uses TinyLlama LLM to analyze sensor data and detect anomalies
"""
import json
import logging
from typing import Dict
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

logger = logging.getLogger('iotshield')

class TinyLlamaAnomalyDetector:
    """Anomaly Detection using TinyLlama LLM"""
    def __init__(self):
        self.model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        logger.info("TinyLlama Anomaly Detector initialized")

    def analyze(self, sensor_data: Dict) -> Dict:
        """
        Analyze IoT sensor data and detect anomalies using TinyLlama.
        Args:
            sensor_data: Dictionary containing sensor information
        Returns:
            Dictionary with fields:
            - anomaly (bool): Whether the data is anomalous
            - explanation (str): Explanation of the analysis
            - severity (str): Severity level [LOW, MEDIUM, HIGH, CRITICAL]
            - suggestion (str): Recommended action
        """
        prompt = self._create_analysis_prompt(sensor_data)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=128)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        result = self._parse_llama_response(response)
        logger.info(f"TinyLlama analysis complete: anomaly={result['anomaly']}")
        return result

    def _create_analysis_prompt(self, sensor_data: Dict) -> str:
        # Use the same prompt logic as before for consistency
        sensor_type = sensor_data.get('sensor_type', 'Unknown')
        value = sensor_data.get('value', 0)
        unit = sensor_data.get('unit', '')
        device_name = sensor_data.get('device_name', 'Unknown Device')
        location = sensor_data.get('location', 'Unknown Location')
        timestamp = sensor_data.get('timestamp', 'Unknown')
        normal_ranges = self._get_normal_ranges(sensor_type)
        prompt = f"""You are an IoT security and monitoring expert. Analyze the following sensor data and determine if it represents an anomaly or normal behavior.\n\n**Sensor Data:**\n- Sensor Type: {sensor_type}\n- Current Value: {value} {unit}\n- Device: {device_name}\n- Location: {location}\n- Timestamp: {timestamp}\n\n**Normal Range Context:**\n{normal_ranges}\n\n**Severity Classification Guidelines:**\n- **LOW**: Minor deviation from normal (5-15% outside normal range). Informational only, no immediate action needed.\n- **MEDIUM**: Moderate deviation (15-30% outside normal range). Monitor closely, may need attention soon.\n- **HIGH**: Significant deviation (30-50% outside normal range) or approaching danger threshold. Requires investigation.\n- **CRITICAL**: Extreme deviation (>50% outside normal range) or exceeds safety threshold. Immediate action required, potential danger.\n\n**Examples:**\n- Temperature 32°C (normal: 20-28°C) → MEDIUM (slightly warm, monitor)\n- Temperature 38°C (normal: 20-28°C) → HIGH (uncomfortably hot, investigate)\n- Temperature 48°C (normal: 20-28°C) → CRITICAL (dangerous heat, immediate action)\n- Humidity 65% (normal: 30-60%) → LOW (slightly high, informational)\n- Gas 0.35 ppm (normal: 0-0.3) → MEDIUM (elevated, monitor for leak)\n- Gas 0.75 ppm (critical: >0.7) → CRITICAL (dangerous leak, evacuate)\n\n**Task:**\nDetermine if this sensor reading is normal or anomalous. Consider:\n1. Is the value within expected range for this sensor type?\n2. How far is it from the normal range (percentage deviation)?\n3. Does it pose an immediate safety risk?\n4. Use LOW/MEDIUM for minor deviations, reserve HIGH/CRITICAL for genuine concerns.\n\n**Required Response Format (JSON only, no markdown):**\n{{\n    \"anomaly\": true/false,\n    \"explanation\": \"Clear explanation of why this is or isn't an anomaly, including deviation percentage if relevant (2-3 sentences)\",\n    \"severity\": \"LOW/MEDIUM/HIGH/CRITICAL\",\n    \"suggestion\": \"Specific action recommendation appropriate to severity level (1-2 sentences)\"\n}}\n\nRespond ONLY with valid JSON. No additional text or formatting.\n"""
        return prompt

    def _get_normal_ranges(self, sensor_type: str) -> str:
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

    def _parse_llama_response(self, response_text: str) -> Dict:
        try:
            cleaned = response_text.strip()
            if cleaned.startswith('```'):
                lines = cleaned.split('\n')
                cleaned = '\n'.join(lines[1:-1] if len(lines) > 2 else lines)
            result = json.loads(cleaned)
            required_fields = ['anomaly', 'explanation', 'severity', 'suggestion']
            for field in required_fields:
                if field not in result:
                    result[field] = self._get_default_value(field)
            return result
        except Exception as e:
            logger.error(f"Failed to parse TinyLlama JSON response: {e}")
            return {
                'anomaly': False,
                'explanation': 'Unable to parse LLM response',
                'severity': 'LOW',
                'suggestion': 'Manual review recommended'
            }

    def _get_default_value(self, field: str):
        defaults = {
            'anomaly': False,
            'explanation': 'Analysis incomplete',
            'severity': 'LOW',
            'suggestion': 'Review sensor data manually'
        }
        return defaults.get(field, '')
