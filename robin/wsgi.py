import os, sys

sys.path.append('/home/pi/Django')
#sys.path.append('/home/pi/Django/robin')
sys.path.append('/home/pi/Django/myvenv/lib/python3.5/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "robin.settings")

application = get_wsgi_application()
