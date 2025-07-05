from datetime import datetime, timezone
import os
from time import sleep

from PIL import Image

from src.background_tasks.celery.app import celery_app
from src.service.file_storage import MediaFileStorageService


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
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)

        # Build image new name
        new_filename = f"{name}_{size}px{ext}"
        new_filename_obj = file_service.FilenameSchema(
            original_filename=new_filename,
            timestamp=datetime.now(timezone.utc).timestamp()
        )

        # New file absolute path
        new_abs_path = file_service.get_abs_filepath(new_filename_obj.storage_filename, not_found_err=False)

        # Save image
        img_resized.save(new_abs_path)
        print(f"Image saved: {new_abs_path}")
