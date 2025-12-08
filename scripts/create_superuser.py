from django.contrib.auth import get_user_model
import django
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path when running from the scripts/ folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'busproject.settings')
django.setup()

User = get_user_model()
username = 'admin'
email = 'admin@example.com'
password = 'password'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created:', username)
else:
    print('Superuser already exists:', username)
