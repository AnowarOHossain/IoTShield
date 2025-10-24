"""
WSGI config for IoTShield project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iotshield_backend.settings')

application = get_wsgi_application()
