import asyncio
from datetime import datetime, timezone
import os
from time import sleep

from PIL import Image

from src.database import async_session_maker_null_pool
from src.background_tasks.celery.app import celery_app
from src.service.file_storage import MediaFileStorageService
from src.utils.db_manager import DBManager


@celery_app.task
def test_task():
    print("Test task started")
    sleep(5)
    print("Test task finished")


@celery_app.task
def resize_image(original_filename: str, rel_path: str):
    file_service = MediaFileStorageService()

    sizes = [300, 200, 100]

    # Open image
    image_abs_path = file_service.get_abs_filepath(rel_path)
    img = Image.open(image_abs_path)

    # Get image name and extension
    name, ext = os.path.splitext(original_filename.strip().lower())

    # Iterate over sizes
    for size in sizes:
        # Resize image
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS
        )

        # Build image new name
        new_filename = f"{name}_{size}px{ext}"
        new_filename_obj = file_service.FilenameSchema(
            original_filename=new_filename,
            timestamp=datetime.now(timezone.utc).timestamp(),
        )

        # New file absolute path
        new_abs_path = file_service.get_abs_filepath(
            new_filename_obj.storage_filename, not_found_err=False
        )

        # Save image
        img_resized.save(new_abs_path)
        print(f"Image saved: {new_abs_path}")


async def get_bookings_with_today_checkin_helper():
    print("Run async check bookings task")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_app.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
