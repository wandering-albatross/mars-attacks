import argparse
import os
import sys

from dependency_injector.wiring import Provide, inject
from mars_attacks.entrypoints.containers import Container
from mars_attacks.tracking.adapters.repositories.invaders import InvadersRepository
from mars_attacks.tracking.adapters.repositories.radar_scan import RadarScansRepository
from mars_attacks.tracking.renderers.base import Renderer
from mars_attacks.tracking.trackers.base import Tracker
from mars_attacks.tracking.use_cases.invaders_tracking import (
    InvadersTrackingInputDto,
    InvadersTrackingUC,
)


@inject
def main(
    invaders_repo: InvadersRepository = Provide[Container.patterns_repository],
    radar_scans_repo: RadarScansRepository = Provide[Container.scans_repository],
    tracker: Tracker = Provide[Container.tracker_service],
    renderer: Renderer = Provide[Container.renderer_service],
) -> None:
    """The main routine."""

    arguments_parser = argparse.ArgumentParser()
    arguments_parser.add_argument("radar_scan", help="Path to a valid radar scan file")

    args = arguments_parser.parse_args()

    radar_scan_file = args.radar_scan
    print(f"Processing radar scan file: {radar_scan_file}")

    tracking_uc = InvadersTrackingUC(
        tracker=tracker,
        renderer=renderer,
        radar_scans_repo=radar_scans_repo,
        invaders_repo=invaders_repo,
    )
    input_dto = InvadersTrackingInputDto(filename=os.path.basename(radar_scan_file))
    tracking_uc.execute(input_dto)


container = Container()
container.init_resources()
container.wire(modules=[__name__])
sys.exit(main())
