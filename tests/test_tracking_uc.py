from typing import List

import pytest
from mars_attacks.tracking.adapters.repositories.invaders import InvadersRepository
from mars_attacks.tracking.adapters.repositories.radar_scan import RadarScansRepository
from mars_attacks.tracking.domain.entities.invader import Invader
from mars_attacks.tracking.domain.entities.radar_scan import RadarScan
from mars_attacks.tracking.domain.value_objects import RadarScanId
from mars_attacks.tracking.renderers.renderers import ConsoleRenderer
from mars_attacks.tracking.trackers.np_tracker import NpTracker
from mars_attacks.tracking.use_cases.invaders_tracking import (
    InvadersTrackingInputDto,
    InvadersTrackingUC,
)


@pytest.fixture
def np_tracker():
    return NpTracker()


class DummyInvadersRepo(InvadersRepository):
    def query(self) -> List[Invader]:
        return [Invader(id="1", pattern="-o-")]


class DummyRadarScanRepo(RadarScansRepository):
    def get(self, radar_scan_id: RadarScanId) -> RadarScan:
        return RadarScan("id", "---\n-o-\n---")


def test_invaders_tracking_uc(capsys):
    tracker = NpTracker(ratio=0.85)
    renderer = ConsoleRenderer()
    invaders_repo = DummyInvadersRepo()
    radar_scans_repo = DummyRadarScanRepo()

    uc = InvadersTrackingUC(
        tracker=tracker,
        renderer=renderer,
        invaders_repo=invaders_repo,
        radar_scans_repo=radar_scans_repo,
    )

    input_dto = InvadersTrackingInputDto(filename="any")

    uc.execute(input_dto)

    captured = capsys.readouterr()
    expected = "---\n-1-\n---\n"
    assert captured.out == expected
