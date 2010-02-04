import os, sys
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT_PATH)
sys.path.append('/usr/lib/python2.6/site-packages/django')
sys.path.append('/var/www/djangoprojects')
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

import bandcontrol.monitor
bandcontrol.monitor.start(interval=1.0)
