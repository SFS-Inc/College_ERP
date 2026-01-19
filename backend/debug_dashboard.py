import os
import django
from django.conf import settings
from django.template.loader import get_template
from django.template import Context, Template

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    print("Attempting to load template 'dashboard.html'...")
    t = get_template('dashboard.html')
    print("Template loaded successfully.")
    print("Attempting to render template...")
    content = t.render({})
    print("Template rendered successfully.")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
