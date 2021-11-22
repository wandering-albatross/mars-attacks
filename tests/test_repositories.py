import pytest
from mars_attacks.tracking.adapters.repositories.invaders import FileInvadersRepository
from mars_attacks.tracking.adapters.repositories.radar_scan import (
    FileRadarScansRepository,
)
from mars_attacks.tracking.domain.entities.invader import Invader
from mars_attacks.tracking.domain.entities.radar_scan import RadarScan


def test_file_invaders_repository_query(tmpdir):
    invaders_data = {
        "invader1.txt": "--oo--o--\n--oo--o--",
        "invader2.txt": "o---o---o\n-ooo-ooo-",
    }
    # Create invader files
    invaders_dir = tmpdir.mkdir("invaders")
    repo = FileInvadersRepository(location=invaders_dir)

    # Ensure no results are returned when there are no files
    invader_patterns = repo.query()
    assert len(invader_patterns) == 0

    # Create files
    for filename, data in invaders_data.items():
        file_obj = invaders_dir.join(filename)
        file_obj.write(data)

    # Ensure 2 invaders are correctly loaded
    invader_patterns = repo.query()
    assert len(invader_patterns) == 2
    assert Invader("invader1.txt", invaders_data["invader1.txt"]) in invader_patterns
    assert Invader("invader2.txt", invaders_data["invader2.txt"]) in invader_patterns


def test_file_radar_scan_repository_get(tmpdir):
    radar_scan_id = "radar_scan1.txt"
    radar_scan_data = {
        radar_scan_id: "--oo--o----oo--o--\n--oo--o----oo--o--",
    }
    # Create radar scan file
    scans_dir = tmpdir.mkdir("radar_scans")
    repo = FileRadarScansRepository(location=scans_dir)

    # Ensure no results are returned when there are no files
    with pytest.raises(FileNotFoundError):
        repo.get(radar_scan_id=radar_scan_id)

    # Create files
    for filename, data in radar_scan_data.items():
        file_obj = scans_dir.join(filename)
        file_obj.write(data)

    # Ensure radar scan is correctly loaded
    radar_scan = repo.get(radar_scan_id=radar_scan_id)
    assert RadarScan(radar_scan_id, radar_scan_data[radar_scan_id]) == radar_scan
