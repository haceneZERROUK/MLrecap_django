import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niab.settings')
django.setup()
from django.contrib.auth import get_user_model

from dotenv import load_dotenv, find_dotenv


dot_env_path = find_dotenv()
load_dotenv(dotenv_path=dot_env_path, override=True)



User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username=os.getenv("USERNAME", "admin"),
        email=os.getenv("EMAIL", "admin"),
        password=os.getenv("PASSWORD", "admin"),
        first_name="admin",
        last_name="admin",
    )
