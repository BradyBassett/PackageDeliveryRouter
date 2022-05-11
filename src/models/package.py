from typing import Optional, TYPE_CHECKING
import re
from datetime import datetime


class Package:
    def __init__(self, package_id: int, address: str, city: str, state: str, zipcode: int, deadline: str, weight: int,
                 special_notes: str) -> None:
        """
        Constructor class to initialize a new package object.\n
        Space-time complexity: O(1)
        """
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
        self.delivery_status: str = "At the hub"
        self.departure_time: Optional[datetime] = None

    def __repr__(self) -> str:
        """
        Repr method to display a package object.\n
        Space-time complexity: O(1)
        """
        representation: str = f"Package {self.package_id}, {self.delivery_status}"
        if self.delivery_deadline:
            representation += f", Deadline {self.delivery_deadline.time()}"
        else:
            representation += ", No deadline"

        if self.departure_time and self.delivery_status != "At the hub":
            representation += f", Departed at {self.departure_time.time()}"

        if self.delivered_time and self.delivery_status == "Delivered":
            representation += f", Delivered at {self.delivered_time.time()}"

        return representation

    def calculate_priority(self) -> int:
        """
        A method to determine a packages priority based on its city in relation to the hub as well as whether it has a
        delivery deadline.\n
        Space-time complexity: O(1)
        """
        priority: int = 0

        # Cities closer to the Hub city will have a lower priority number
        cities = {
            "Salt Lake City": 0,
            "Millcreek": 10,
            "West Valley City": 20,
            "Holladay": 30,
            "Murray": 40
        }

        # Prioritize nodes with a delivery deadline over nodes without
        if self.delivery_deadline is not None:
            priority -= 20

        return priority + cities[self.city]


def get_deadline(deadline: str) -> Optional[datetime]:
    """
    A method to calculate the datetime deadline of a package based on a given string representing the deadline.\n
    Space-time complexity: O(1)
    """
    if deadline == "EOD":
        return None

    temp = re.split("[: ]", deadline)
    if temp[2] == "PM":
        temp[0] += 12

    return datetime.now().replace(hour=int(temp[0]), minute=int(temp[1]), second=0, microsecond=0)
