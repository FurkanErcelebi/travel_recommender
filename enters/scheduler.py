
import logging
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import register_events
from django.utils import timezone
import sys

scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)
# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def show_time_zone():
    today = timezone.now()
    print('time {}'.format(today))


def start():
    if settings.DEBUG:
      	# Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    
    scheduler.add_job(show_time_zone, trigger = CronTrigger(second="*/10"), name='show_time_outs', jobstore='default',)
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)