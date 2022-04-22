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

    def calculate_priority(self) -> int:
        priority: int = 0

        cities = {
            "Salt Lake City": 8,
            "West Valley City": 6,
            "Millcreek": 4,
            "Holladay": 2,
            "Murray": 0
        }

        if self.delivery_deadline is not None:
            priority -= 5

        if self.package_id in [13, 15, 19]:
            priority = -8
            self.special_notes = " "

        if self.special_notes == "Delayed on flight---will not arrive to depot until 9:05 am":
            priority += 8
        elif self.special_notes == "Wrong address listed":
            priority += 6
        elif "Must be delivered with" in self.special_notes:
            priority -= 10
        elif self.special_notes == "Can only be on truck 2":
            priority -= 10

        return priority + cities[self.city]


def get_deadline(deadline: str) -> Optional[datetime]:
    if deadline == "EOD":
        return None

    temp = re.split("[: ]", deadline)
    if temp[2] == "PM":
        temp[0] += 12

    return datetime(datetime.now().year, datetime.now().month, datetime.now().day, int(temp[0]), int(temp[1]))
