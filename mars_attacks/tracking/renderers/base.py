import abc
from typing import Any, Dict, List

from mars_attacks.tracking.domain.entities.radar_scan import RadarScan


class Renderer(abc.ABC):
    @abc.abstractmethod
    def render(self, radar_scan: RadarScan, matches: List[Dict[str, Any]]) -> None:
        """Render matches on the image."""
        pass
