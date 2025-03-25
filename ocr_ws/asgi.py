"""
ASGI config for ocr_ws project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocr_ws.settings')

application = get_asgi_application()
