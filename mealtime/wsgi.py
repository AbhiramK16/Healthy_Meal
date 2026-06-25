"""
WSGI config for mealtime project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mealtime.settings')

application = get_wsgi_application()

# Run migrations on cold start if using a writable database (PostgreSQL)
from django.conf import settings
if 'sqlite3' not in settings.DATABASES['default']['ENGINE']:
    from django.core.management import call_command
    call_command('migrate', '--noinput')

app = application
