import os
import sys

path = '/home/oren/src/chat/ChatSite'
if path not in sys.path:
    sys.path.append( path )

os.environ[ 'DJANGO_SETTINGS_MODULE' ] = 'ChatSite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()