"""
WSGI config for boekensite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

if "/home/pi/library" not in sys.path:
    sys.path.append("/home/pi/library/")


os.environ['DJANGO_SETTINGS_MODULE'] =  'boekensite.settings'

application = get_wsgi_application()
