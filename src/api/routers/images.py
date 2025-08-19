from fastapi import APIRouter, HTTPException, UploadFile, status

from src.services.file_storage import MediaFileStorageService
from src.background_tasks.celery.tasks import resize_image
from src.utils.responses import build_protected_file_redirect_response

router = APIRouter(prefix="/images", tags=["Images"])


@router.get("/{filepath}")
def get_image(filepath: str):
    # return special redirect response for NGINX
    return build_protected_file_redirect_response(filepath)


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
