import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chainstory.settings')

import django
django.setup()

from channels.routing import get_default_application
application = get_default_application()
app = application