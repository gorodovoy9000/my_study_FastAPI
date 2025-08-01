from celery import Celery

from src.config import settings

celery_app = Celery(
    "celery_tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.background_tasks.celery.tasks",
    ],
)

celery_app.conf.beat_schedule = {
    "check_today_bookings": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}
