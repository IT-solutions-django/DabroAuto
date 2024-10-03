import os
from celery import Celery

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

app = Celery("car_seller")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
