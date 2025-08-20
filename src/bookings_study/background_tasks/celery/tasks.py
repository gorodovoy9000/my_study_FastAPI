import asyncio
from datetime import datetime, timezone
import logging
import os
from time import sleep

from PIL import Image

from bookings_study.database import async_session_maker_null_pool
from bookings_study.background_tasks.celery.app import celery_app
from bookings_study.services.file_storage import MediaFileStorageService
from bookings_study.utils.db_manager import DBManager


@celery_app.task
def test_task():
    print("Test task started")
    sleep(5)
    print("Test task finished")


@celery_app.task
def resize_image(original_filename: str, rel_path: str):
    logging.debug(f"Run background task resize_image with {original_filename=} and {rel_path=}")
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
        logging.info(f"Image saved on path {new_abs_path}")


async def get_bookings_with_today_checkin_helper():
    logging.debug("Run background task get_bookings_with_today_checkin_helper")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        logging.debug(f"Got {bookings=}")


@celery_app.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
