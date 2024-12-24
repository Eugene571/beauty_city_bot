
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_bot.settings')
django.setup()
from bot.models import Specialist


masters = Specialist.objects.get(id=36)
print(masters)
