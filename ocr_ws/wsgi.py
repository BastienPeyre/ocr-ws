"""
WSGI config for ocr_ws project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocr_ws.settings')

application = get_wsgi_application()
