from celery import Celery

from src.config import settings

celery_app = Celery(
    "celery_tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.background_tasks.celery.tasks",
    ],
)
