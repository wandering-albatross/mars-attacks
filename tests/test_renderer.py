import pytest
from mars_attacks.tracking.domain.entities.radar_scan import RadarScan
from mars_attacks.tracking.renderers.renderers import ConsoleRenderer
from mars_attacks.tracking.trackers.np_tracker import NpTracker


@pytest.fixture
def np_tracker():
    return NpTracker()


def test_renderer(np_tracker, capsys):
    radar_scan = "---o---\n---o---\n-------"
    matches = [
        {
            "name": "invader1",
            "start_row": 0,
            "end_row": 2,
            "start_col": 2,
            "end_col": 4,
        },
        {
            "name": "invader2",
            "start_row": 0,
            "end_row": 2,
            "start_col": 3,
            "end_col": 5,
        },
    ]
    renderer = ConsoleRenderer()
    renderer.render(RadarScan("1", scan=radar_scan), matches)
    # assert console renderer printed output to the console
    captured = capsys.readouterr()
    expected = "---1---\n---1---\n-------\n"
    assert captured.out == expected
