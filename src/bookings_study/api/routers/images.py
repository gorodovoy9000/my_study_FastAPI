from fastapi import APIRouter, UploadFile

from bookings_study.api.exceptions import MediaFilenameInvalidHTTPException
from bookings_study.services.file_storage import MediaFileStorageService
from bookings_study.services.exceptions import MediaFilenameInvalidException
from bookings_study.background_tasks.celery.tasks import resize_image
from bookings_study.utils.responses import build_protected_file_redirect_response

router = APIRouter(prefix="/images", tags=["Images"])


@router.get("/{filepath:path}", description="Download via redirect to NGINX")
def get_image(filepath: str):
    # return special redirect response for NGINX
    return build_protected_file_redirect_response(filepath)


@router.post("", description="Upload via FastAPI")
def upload_image(file: UploadFile):
    filename = file.filename
    file_object = file.file
    # write file and catch validation error
    try:
        rel_filepath = MediaFileStorageService().create_file(filename, file_object)
    except MediaFilenameInvalidException:
        raise MediaFilenameInvalidHTTPException
    # background task - save resized image copies
    resize_image.delay(filename, rel_filepath)
    return {"status": "Ok", "filepath": rel_filepath}
