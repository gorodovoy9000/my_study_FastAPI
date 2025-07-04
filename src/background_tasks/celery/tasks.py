from time import sleep

from src.background_tasks.celery.app import celery_app


@celery_app.task
def test_task():
    print("Test task started")
    sleep(5)
    print("Test task finished")
