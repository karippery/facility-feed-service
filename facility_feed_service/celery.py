import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "facility_feed_service.settings")
app = Celery("facility_feed_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
