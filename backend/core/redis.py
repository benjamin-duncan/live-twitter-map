import os

from redis import Redis
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
