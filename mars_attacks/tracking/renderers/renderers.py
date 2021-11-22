from typing import Any, Dict, List

from mars_attacks.tracking.domain.entities.radar_scan import RadarScan
from mars_attacks.tracking.renderers.base import Renderer


class ConsoleRenderer(Renderer):
    def render(self, radar_scan: RadarScan, matches: List[Dict[str, Any]]) -> None:
        """Render matches on the image."""

        image_str_list = radar_scan.scan.splitlines()
        ids = {}
        counter = 0
        for match in matches:
            symbol = ids.get(match.get("name"))
            if not symbol:
                counter += 1
                symbol = ids[match.get("name")] = str(counter)

            for row in range(match.get("start_row"), match.get("end_row")):
                substring = image_str_list[row][
                    match.get("start_col") : match.get("end_col")
                ].replace("o", symbol)
                image_str_list[row] = (
                    str(image_str_list[row][0 : match.get("start_col")])
                    + substring
                    + str(image_str_list[row][match.get("end_col") :])
                )
        print("\n".join(image_str_list).replace("o", "-"))
