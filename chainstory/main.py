import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chainstory.settings')

import django
django.setup()

from chainstory.asgi import application
app = application 