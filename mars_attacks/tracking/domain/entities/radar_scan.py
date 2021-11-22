from dataclasses import dataclass
from typing import Optional

from mars_attacks.tracking.domain.value_objects import RadarScanData, RadarScanId


@dataclass
class RadarScan:
    id: Optional[RadarScanId]
    scan: RadarScanData
