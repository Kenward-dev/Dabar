"""This module initializes the Celery application for the Taskly API project."""

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskly_api.settings')
app = Celery('taskly_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()