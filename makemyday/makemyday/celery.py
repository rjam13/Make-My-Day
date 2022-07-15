# here so that celery module will not clash with library
from __future__ import absolute_import, unicode_literals

import os
import sys

from celery import Celery

# setting django settings module environment variable for the celery command line program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'makemyday.settings')

app = Celery('makemyday')
app.conf.enable_utc = False
app.conf.timezone = 'US/Eastern'

# adding django settings module as a configuration source for celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto discovers task in any applications and import those tasks for celery to run
app.autodiscover_tasks()
