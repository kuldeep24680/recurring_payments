from __future__ import absolute_import

from celery import Celery

from oracle import mainapp as app


def make_celery(task_name, broker, result_backend):
    celery = Celery(task_name, broker=broker)
    celery.conf.update({"task_ignore_result": True})

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
