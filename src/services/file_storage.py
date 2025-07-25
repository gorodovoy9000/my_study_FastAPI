from datetime import datetime, timezone
import re
import typing

from pydantic import BaseModel, computed_field, field_validator

from src.config import settings
from src.services.base import BaseService
from src.utils.file_manager import LocalFileManager


# filename format "timestamp--version--filename"
class Filename(BaseModel):
    original_filename: str
    timestamp: float
    version: int = 0  # reserved for already exists cases

    @computed_field
    @property
    def storage_filename(self) -> str:
        return f"{self.timestamp}--{self.version}--{self.original_filename}"

    @field_validator("original_filename", mode="before")
    @classmethod
    def validate_filename(cls, filename: str) -> str:
        # valid examples - name.ext, name1.ext, some_name.ext1, name
        pattern = re.compile(r"[a-z0-9_]+(?:\.[a-z0-9]+)?")
        match = re.fullmatch(pattern, filename)
        if not match:
            msg = (
                f"Invalid filename: {filename}\n"
                f"Only allowed lower latin letters(a-z), digits, underscore "
                f"and optional extension after dot(.)\n"
                f"Examples: file1.txt, some_image.jpg some_file etc"
            )
            raise ValueError(msg)
        return filename


class MediaFilename(Filename):
    @field_validator("original_filename", mode="before")
    @classmethod
    def validate_filename(cls, filename: str) -> str:
        # valid examples - name.ext, name1.ext, some_name.ext1
        pattern = re.compile(r"[a-z0-9_]+\.[a-z0-9]+")
        match = re.fullmatch(pattern, filename)
        if not match:
            msg = (
                f"Invalid media filename: {filename}\n"
                f"Only allowed lower latin letters(a-z), digits, underscore "
                f"and extension after dot(.)\n"
                f"Examples: image1.png, some_image.jpg etc"
            )
            raise ValueError(msg)
        return filename


class FileStorageService(BaseService):
    root_path: str
    manager: LocalFileManager
    FilenameSchema: type[Filename]

    def get_abs_filepath(self, rel_filepath: str, not_found_err=True) -> str:
        # just return absolute file path
        return self.manager.get_abs_filepath(rel_filepath, not_found_err)

    def create_file(self, original_filename: str, data: typing.BinaryIO):
        # build storage filename
        filename_obj = self.FilenameSchema(
            original_filename=original_filename.strip().lower(),
            timestamp=datetime.now(timezone.utc).timestamp(),
        )
        # write file via manager
        self.manager.write(filename_obj.storage_filename, data)
        # todo write already exists logic?
        # return relative path
        return filename_obj.storage_filename


class MediaFileStorageService(FileStorageService):
    root_path = settings.LOCAL_MEDIA_ROOT
    manager = LocalFileManager(root_path)
    FilenameSchema = MediaFilename
