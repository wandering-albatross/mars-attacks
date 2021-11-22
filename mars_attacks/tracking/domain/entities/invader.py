from dataclasses import dataclass
from typing import Optional

from mars_attacks.tracking.domain.value_objects import InvaderId, InvaderPattern


@dataclass
class Invader:
    id: Optional[InvaderId]
    pattern: InvaderPattern
