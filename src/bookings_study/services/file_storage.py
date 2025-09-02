import re
import typing

from bookings_study.config import settings
from bookings_study.services.base import BaseService
from bookings_study.services.exceptions import (
    FilenameInvalidException,
    MediaFilenameInvalidException,
)
from bookings_study.utils.file_manager import LocalFileManager


class FileStorageService(BaseService):
    manager: LocalFileManager

    def create_file(self, original_filename: str, file: typing.BinaryIO):
        filename = original_filename.lower()
        # validate filename
        self.validate_filename(filename)
        # for now - just read all file data in memory and write
        data = file.read()
        # return relative path
        return self.manager.write(filename, data)

    def validate_filename(self, filename: str) -> None:
        # valid examples - name.ext, name1.ext, some_name.ext1, name
        pattern = re.compile(r"[a-z0-9_]+(?:\.[a-z0-9]+)?")
        match = re.fullmatch(pattern, filename)
        if not match:
            raise FilenameInvalidException


class MediaFileStorageService(FileStorageService):
    manager = LocalFileManager(settings.LOCAL_MEDIA_ROOT)

    def validate_filename(self, filename: str) -> None:
        # valid examples - name.jpg, name1.png, some_name.webp
        allowed_extensions = "|".join(
            ("jpg", "jpeg", "png", "gif", "svg", "webp", "apng", "avif")
        )
        pattern = re.compile(rf"[a-z0-9_]+\.(?:{allowed_extensions})")
        match = re.fullmatch(pattern, filename)
        if not match:
            raise MediaFilenameInvalidException
