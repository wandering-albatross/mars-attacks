import abc

from mars_attacks.foundation.file_storage import FileStorage
from mars_attacks.tracking.domain.entities.radar_scan import RadarScan
from mars_attacks.tracking.domain.value_objects import RadarScanId


class RadarScansRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, radar_scan_id: RadarScanId) -> RadarScan:
        pass


class FileRadarScansRepository(RadarScansRepository, FileStorage):
    """Filesystem based Radar scans repository."""

    def get(self, radar_scan_id: RadarScanId) -> RadarScan:
        return self._to_entity(
            radar_scan_id=radar_scan_id, data=self.read_file(filename=radar_scan_id)
        )

    def _to_entity(self, radar_scan_id: RadarScanId, data: str) -> RadarScan:
        return RadarScan(id=radar_scan_id, scan=data)
