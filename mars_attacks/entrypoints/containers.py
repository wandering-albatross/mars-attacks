from dependency_injector import containers, providers
from mars_attacks.tracking.adapters.repositories.invaders import FileInvadersRepository
from mars_attacks.tracking.adapters.repositories.radar_scan import (
    FileRadarScansRepository,
)
from mars_attacks.tracking.renderers.renderers import ConsoleRenderer
from mars_attacks.tracking.trackers.np_tracker import NpTracker


class Container(containers.DeclarativeContainer):
    """Dependency injector container."""

    config = providers.Configuration(ini_files=["config.ini"])

    # Gateways
    scans_repository = providers.Singleton(
        FileRadarScansRepository,
        location=config.repository.radar_scans_dir,
    )

    patterns_repository = providers.Singleton(
        FileInvadersRepository,
        location=config.repository.patterns_dir,
    )

    # Services
    tracker_service = providers.Factory(
        NpTracker, ratio=config.tracker.ratio.as_float()
    )

    renderer_service = providers.Factory(
        ConsoleRenderer,
    )
