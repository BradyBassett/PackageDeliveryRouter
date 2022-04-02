from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Package:
    package_id: int
    address: str
    city: str
    state: str
    zip: int
    delivery_deadline: str
    weight: int
    delivery_time: Optional[datetime] = None
    special_notes: str = ""
