"""
Email Alert Service for IoTShield
Sends email notifications for critical anomalies detected by the system.
"""

import logging
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime

logger = logging.getLogger('iotshield')


def send_alert_email(alert_data):
    """
    Send email notification for an alert.
    
    Args:
        alert_data (dict): Alert information containing:
            - device_name: Device identifier
            - severity: Alert severity (CRITICAL, HIGH, MEDIUM, LOW)
            - sensor_type: Type of sensor that triggered the alert
            - sensor_value: Current sensor reading
            - description: AI-generated alert description
            - timestamp: When the alert occurred
            - additional_data: Other sensor readings (dict)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    # Check if email alerts are enabled
    if not getattr(settings, 'EMAIL_ALERT_ENABLED', True):
        logger.info("Email alerts are disabled in settings")
        return False
    
    # Check if this severity should trigger an email
    severity = alert_data.get('severity', 'MEDIUM')
    alert_severities = getattr(settings, 'EMAIL_ALERT_SEVERITIES', ['CRITICAL', 'HIGH'])
    
    if severity not in alert_severities:
        logger.debug(f"Skipping email for {severity} alert (not in {alert_severities})")
        return False
    
    try:
        # Prepare email content
        subject = f"🚨 {severity} Alert: {alert_data.get('sensor_type', 'Anomaly')} Detected - {alert_data.get('device_name', 'Unknown Device')}"
        
        # Build email body
        email_body = _build_email_body(alert_data)
        
        # Get recipient email
        recipient_email = getattr(settings, 'ALERT_RECIPIENT_EMAIL', settings.EMAIL_HOST_USER)
        
        # Send email
        send_mail(
            subject=subject,
            message=strip_tags(email_body),  # Plain text version
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=email_body,  # HTML version
            fail_silently=False,
        )
        
        logger.info(f"Alert email sent successfully to {recipient_email} for {severity} alert")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send alert email: {str(e)}")
        return False


def _build_email_body(alert_data):
    """
    Build HTML email body for the alert.
    
    Args:
        alert_data (dict): Alert information
    
    Returns:
        str: HTML formatted email body
    """
    
    severity = alert_data.get('severity', 'MEDIUM')
    device_name = alert_data.get('device_name', 'Unknown Device')
    sensor_type = alert_data.get('sensor_type', 'Unknown Sensor')
    sensor_value = alert_data.get('sensor_value', 'N/A')
    description = alert_data.get('description', 'No description available')
    timestamp = alert_data.get('timestamp', datetime.now())
    additional_data = alert_data.get('additional_data', {})
    
    # Severity color mapping
    severity_colors = {
        'CRITICAL': '#DC2626',  # Red
        'HIGH': '#EA580C',      # Orange
        'MEDIUM': '#CA8A04',    # Yellow
        'LOW': '#16A34A'        # Green
    }
    
    severity_color = severity_colors.get(severity, '#6B7280')
    
    # Severity emoji mapping
    severity_emojis = {
        'CRITICAL': '🚨',
        'HIGH': '⚠️',
        'MEDIUM': '⚡',
        'LOW': 'ℹ️'
    }
    
    severity_emoji = severity_emojis.get(severity, '📊')
    
    # Build sensor readings section
    sensor_readings_html = ""
    if additional_data:
        sensor_readings_html = "<h3 style='color: #374151; margin-top: 20px;'>📊 All Sensor Readings</h3><ul style='list-style: none; padding: 0;'>"
        for key, value in additional_data.items():
            sensor_readings_html += f"<li style='padding: 5px 0;'><strong>{key}:</strong> {value}</li>"
        sensor_readings_html += "</ul>"
    
    # HTML email template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, {severity_color} 0%, {severity_color}dd 100%);
                color: white;
                padding: 30px;
                border-radius: 10px 10px 0 0;
                text-align: center;
            }}
            .content {{
                background: #f9fafb;
                padding: 30px;
                border: 1px solid #e5e7eb;
                border-top: none;
                border-radius: 0 0 10px 10px;
            }}
            .alert-box {{
                background: white;
                border-left: 4px solid {severity_color};
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            .info-row {{
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #e5e7eb;
            }}
            .info-row:last-child {{
                border-bottom: none;
            }}
            .label {{
                font-weight: 600;
                color: #6B7280;
            }}
            .value {{
                color: #111827;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e5e7eb;
                color: #6B7280;
                font-size: 14px;
            }}
            .button {{
                display: inline-block;
                background-color: {severity_color};
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 6px;
                margin-top: 20px;
                font-weight: 600;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1 style="margin: 0; font-size: 28px;">{severity_emoji} IoTShield Alert</h1>
            <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.95;">{severity} Priority</p>
        </div>
        
        <div class="content">
            <div class="alert-box">
                <h2 style="margin-top: 0; color: {severity_color};">{sensor_type} Anomaly Detected</h2>
                
                <div class="info-row">
                    <span class="label">🏠 Device:</span>
                    <span class="value">{device_name}</span>
                </div>
                
                <div class="info-row">
                    <span class="label">📍 Sensor Type:</span>
                    <span class="value">{sensor_type}</span>
                </div>
                
                <div class="info-row">
                    <span class="label">📈 Current Reading:</span>
                    <span class="value" style="color: {severity_color}; font-weight: 600;">{sensor_value}</span>
                </div>
                
                <div class="info-row">
                    <span class="label">⏰ Time:</span>
                    <span class="value">{timestamp}</span>
                </div>
                
                <div class="info-row">
                    <span class="label">🔍 Severity:</span>
                    <span class="value" style="color: {severity_color}; font-weight: 600;">{severity}</span>
                </div>
            </div>
            
            <h3 style="color: #374151; margin-top: 30px;">🤖 AI Analysis</h3>
            <div style="background: white; padding: 15px; border-radius: 5px; border: 1px solid #e5e7eb;">
                <p style="margin: 0; color: #4B5563;">{description}</p>
            </div>
            
            {sensor_readings_html}
            
            <div style="text-align: center;">
                <a href="http://localhost:8000/alerts/" class="button">View in Dashboard</a>
            </div>
        </div>
        
        <div class="footer">
            <p style="margin: 5px 0;">🛡️ <strong>IoTShield</strong> - AI-Powered IoT Security System</p>
            <p style="margin: 5px 0; font-size: 12px;">This is an automated alert from your IoTShield system.</p>
            <p style="margin: 5px 0; font-size: 12px;">Powered by Google Gemini 2.5 Flash AI</p>
        </div>
    </body>
    </html>
    """
    
    return html_content


def test_email_configuration():
    """
    Test email configuration by sending a test email.
    
    Returns:
        bool: True if test email sent successfully
    """
    
    test_alert = {
        'device_name': 'Test Device',
        'severity': 'CRITICAL',
        'sensor_type': 'Temperature',
        'sensor_value': '45°C',
        'description': 'This is a test email from IoTShield to verify email configuration is working correctly.',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'additional_data': {
            'Temperature': '45°C',
            'Humidity': '55%',
            'Gas': '0.2 ppm',
            'Motion': 'No motion detected'
        }
    }
    
    logger.info("Sending test email...")
    success = send_alert_email(test_alert)
    
    if success:
        logger.info("✅ Test email sent successfully!")
    else:
        logger.error("❌ Failed to send test email")
    
    return success
