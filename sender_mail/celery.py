import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sender_mail.settings")
app = Celery("sender_mail")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()