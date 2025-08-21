from datetime import datetime, timezone
import pathlib

from bookings_study.exceptions import FileAlreadyExistsException, FileNotFoundException


class LocalFileManager:
    def __init__(self, storage_root: str):
        self.storage_root = pathlib.PurePath(storage_root)

    def get_abs_filepath(self, rel_filepath: str, not_found_err=True) -> str:
        # build absolute filepath
        abs_filepath =  pathlib.Path(self.storage_root, rel_filepath)
        # raise exception if not found
        if not_found_err and not abs_filepath.is_file():
            raise FileNotFoundException
        return abs_filepath.__str__()

    def write(self, filename: str, data: bytes) -> str:
        # build relative filepath
        storage_filename = self.build_storage_filename(filename)
        relative_filepath = self.build_storage_relative_path(storage_filename)
        # build absolute filepath
        abs_filepath = pathlib.Path(self.storage_root, relative_filepath)
        # raise exception if already exists
        if abs_filepath.is_file():
            raise FileAlreadyExistsException
        # ensure dirs exist
        abs_filepath.parent.mkdir(parents=True, exist_ok=True)
        # write file
        # for now just read in memory and write
        with abs_filepath.open("wb") as f:
            f.write(data)
        return relative_filepath.__str__()

    def build_abs_filepath_from_filename(self, filename: str) -> str:
        storage_filename = self.build_storage_filename(filename)
        storage_relative_filepath = self.build_storage_relative_path(storage_filename)
        abs_filepath = pathlib.Path(self.storage_root, storage_relative_filepath)
        return abs_filepath.__str__()

    def build_storage_filename(self, filename: str, version: int = 0) -> str:
        # storage filename format "timestamp--version--filename"
        timestamp = datetime.now(timezone.utc).timestamp()
        storage_filename = f"{timestamp}--{version}--{filename}"
        return storage_filename

    def build_storage_relative_path(self, filename: str) -> pathlib.PurePath:
        date_now = datetime.now(timezone.utc).date().isoformat()
        storage_relative_path = pathlib.PurePath(date_now, filename)
        return storage_relative_path
