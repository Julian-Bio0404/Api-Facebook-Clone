"""Celery app config."""

from __future__ import absolute_import, unicode_literals

# Utilities
import os

# Celery
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_settings.settings')

app = Celery('facebook', include=['taskapp.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'add-every-1-day': {
            'task': 'taskapp.tasks.notifications.delete_notifications',
            'schedule': crontab(minute=0, hour=0)
        }
    }

app.autodiscover_tasks()


if __name__ == '__main__':
    app.start()
