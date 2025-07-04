import pathlib
import typing

from src.exceptions import FileAlreadyExistsException, FileNotFoundException


class LocalFileManager:
    def __init__(self, storage_root: str):
        self.storage_root = pathlib.Path(storage_root)

    def get_abs_filepath(self, rel_filepath: str) -> str:
        # build absolute filepath
        abs_filepath = self.storage_root.joinpath(rel_filepath)
        # raise exception if not found
        if not abs_filepath.is_file():
            raise FileNotFoundException
        return str(abs_filepath)

    def write(self, rel_filepath: str, data: typing.BinaryIO):
        # build absolute filepath
        abs_filepath = self.storage_root.joinpath(rel_filepath)
        # raise exception if already exists
        if abs_filepath.is_file():
            raise FileAlreadyExistsException
        # write file
        # for now just read in memory and write
        with abs_filepath.open('wb') as f:
            f.write(data.read())
