"""Custom logger for IoTShield"""

import logging
import json
from datetime import datetime


class IoTShieldLogger:
    """Custom logger with database integration"""
    
    def __init__(self, name='iotshield'):
        self.logger = logging.getLogger(name)
    
    def log_to_db(self, level, module, message, details=None):
        """Log message to database"""
        from dashboard.models import SystemLog
        
        try:
            SystemLog.objects.create(
                level=level.upper(),
                module=module,
                message=message,
                details=details or {}
            )
        except Exception as e:
            self.logger.error(f"Failed to log to database: {e}")
    
    def info(self, message, module='system', details=None):
        """Log info message"""
        self.logger.info(message)
        self.log_to_db('INFO', module, message, details)
    
    def warning(self, message, module='system', details=None):
        """Log warning message"""
        self.logger.warning(message)
        self.log_to_db('WARNING', module, message, details)
    
    def error(self, message, module='system', details=None):
        """Log error message"""
        self.logger.error(message)
        self.log_to_db('ERROR', module, message, details)
    
    def critical(self, message, module='system', details=None):
        """Log critical message"""
        self.logger.critical(message)
        self.log_to_db('CRITICAL', module, message, details)


# Global logger instance
iot_logger = IoTShieldLogger()
