import abc
from typing import Any, Dict, List


class Tracker(abc.ABC):
    @abc.abstractmethod
    def search(
        self, image: Dict, patterns: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Search for occurrences of patterns in the image."""
        pass
