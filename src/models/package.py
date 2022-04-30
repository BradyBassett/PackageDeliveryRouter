from typing import Optional
import re
from datetime import datetime


class Package:
    def __init__(self, package_id: int, address: str, city: str, state: str, zipcode: int, deadline: str, weight: int,
                 special_notes: str) -> None:
        self.package_id: int = package_id
        self.address: str = address
        self.city: str = city
        self.state: str = state
        self.zipcode: int = zipcode
        self.delivery_deadline: Optional[datetime] = get_deadline(deadline)
        self.weight: int = weight
        self.special_notes: str = special_notes
        self.priority: int = self.calculate_priority()
        self.delivered_time: Optional[datetime] = None

    def __repr__(self) -> str:
        return f"\n{self.package_id}, {self.address}, {self.city}, {self.state}, {self.zipcode}, {self.priority}, " \
               f"{self.delivery_deadline}, {self.special_notes}"

    # TODO - Continue to optimize package priorities
    def calculate_priority(self) -> int:
        priority: int = 0

        cities = {
            "Salt Lake City": 0,
            "Millcreek": 5,
            "West Valley City": 10,
            "Holladay": 12.5,
            "Murray": 15
        }

        if self.delivery_deadline is not None:
            priority -= 5

        if self.package_id in [13, 15, 19]:
            priority -= 20

        if self.special_notes == "Delayed on flight---will not arrive to depot until 9:05 am":
            priority += 25
        elif self.special_notes == "Wrong address listed":
            priority += 35
        elif "Must be delivered with" in self.special_notes:
            priority -= 20

        return priority + cities[self.city]


def get_deadline(deadline: str) -> Optional[datetime]:
    if deadline == "EOD":
        return None

    temp = re.split("[: ]", deadline)
    if temp[2] == "PM":
        temp[0] += 12

    return datetime.now().replace(hour=int(temp[0]), minute=int(temp[1]), second=0, microsecond=0)
