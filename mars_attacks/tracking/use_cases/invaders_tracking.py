from dataclasses import dataclass

from mars_attacks.tracking.adapters.repositories.invaders import InvadersRepository
from mars_attacks.tracking.adapters.repositories.radar_scan import RadarScansRepository
from mars_attacks.tracking.renderers.renderers import Renderer
from mars_attacks.tracking.trackers.base import Tracker


@dataclass
class InvadersTrackingInputDto:
    filename: str


class InvadersTrackingUC:
    def __init__(
        self,
        tracker: Tracker,
        renderer: Renderer,
        radar_scans_repo: RadarScansRepository,
        invaders_repo: InvadersRepository,
    ) -> None:
        self.tracker = tracker
        self.renderer = renderer
        self.radar_scans_repo = radar_scans_repo
        self.invaders_repo = invaders_repo

    def execute(self, input_dto: InvadersTrackingInputDto) -> None:
        """Run actual business logic - tracking invaders on the radar scan."""
        # Read scans from abstract repositories. We don't care here about whether those are
        # filesystem, database, API etc. based.
        radar_scan = self.radar_scans_repo.get(radar_scan_id=input_dto.filename)
        invaders = self.invaders_repo.query()

        # Tracking logic
        scan_image = {"name": radar_scan.id, "image": radar_scan.scan}
        patterns = [
            {"name": invader.id, "image": invader.pattern} for invader in invaders
        ]
        matches = self.tracker.search(image=scan_image, patterns=patterns)

        # Present results. It's up to the renderer to decide about how to do it.
        self.renderer.render(radar_scan, matches)
