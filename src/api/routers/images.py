from fastapi import APIRouter, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from src.exceptions import FileNotFoundException
from src.services.file_storage import MediaFileStorageService
from src.background_tasks.celery.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Images"])


@router.get("/{filepath}")
def get_image(filepath: str):
    try:
        abs_filepath = MediaFileStorageService().get_abs_filepath(filepath)
        return FileResponse(abs_filepath)
    except FileNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )


@router.post("")
def upload_image(file: UploadFile):
    filename = file.filename
    file_object = file.file
    # write file and catch validation error
    try:
        rel_filepath = MediaFileStorageService().create_file(filename, file_object)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(err),
        )

    # background task - save resized image copies
    resize_image.delay(filename, rel_filepath)
    return {"status": "Ok"}
