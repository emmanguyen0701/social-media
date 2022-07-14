import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialnetwork.settings')

# app = Celery('socialapp', backend='redis://localhost' , broker='redis://localhost')
app = Celery('socialapp', backend='redis://:pa7610f9aaa770e797ff9cdb4666ba63795759e917135f6c00ceb4a14b64ba5d4@ec2-3-218-215-107.compute-1.amazonaws.com:9380', 
broker='redis://:pa7610f9aaa770e797ff9cdb4666ba63795759e917135f6c00ceb4a14b64ba5d4@ec2-3-218-215-107.compute-1.amazonaws.com:9380')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')