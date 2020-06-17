from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery import Celery

app = Celery('tasks', broker='amqp://localhost//')


@app.task
def test_task():
    print('testing celery task')
    return
