import abc
from typing import List

from mars_attacks.foundation.file_storage import FileStorage
from mars_attacks.tracking.domain.entities.invader import Invader
from mars_attacks.tracking.domain.value_objects import InvaderId


class InvadersRepository(abc.ABC):
    @abc.abstractmethod
    def query(self) -> List[Invader]:
        pass


class FileInvadersRepository(InvadersRepository, FileStorage):
    """Filesystem based Invader patterns repository."""

    ALLOWED_EXTENSION: str = ".txt"

    def query(self) -> List[Invader]:
        return [
            self._to_entity(filename, self.read_file(filename))
            for filename in self._list_files()
        ]

    def _list_files(self) -> List[str]:
        return [
            filename
            for filename in super().list_files()
            if self._is_valid_file(filename)
        ]

    def _is_valid_file(self, filename: str) -> bool:
        return filename.endswith(self.ALLOWED_EXTENSION)

    def _to_entity(self, invader_id: InvaderId, data: str) -> Invader:
        return Invader(id=invader_id, pattern=data)
