import os
from typing import List


class FileStorage:
    def __init__(self, location):
        self.location = location

    def _get_path(self, filename: str) -> str:
        return os.path.join(self.location, filename)

    def read_file(self, filename: str) -> str:
        path = self._get_path(filename)
        try:
            with open(path, "r") as file:
                data = file.read()
        except OSError as e:
            raise e
        else:
            return data

    def _is_valid_file(self, filename):
        return os.path.isfile(self._get_path(filename))

    def list_files(self) -> List[str]:
        return [
            filename
            for filename in os.listdir(self.location)
            if self._is_valid_file(filename)
        ]

    def save(self, filename: str, data: str) -> None:
        path = self._get_path(filename)
        try:
            with open(path, "w") as file:
                for line in data:
                    file.write(line + "\n")
        except OSError as e:
            raise e
