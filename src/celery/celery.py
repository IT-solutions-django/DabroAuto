import os
from celery import Celery

os.environ["DJANGO_SETTINGS_MODULE"] = "src.config.settings"

app = Celery("car_seller")

app.config_from_object(f"django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
