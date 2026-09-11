import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

_src_dir = Path(__file__).resolve().parent.parent
if str(_src_dir) not in sys.path:
    sys.path.insert(0, str(_src_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cofig.settings')

application = get_wsgi_application()

