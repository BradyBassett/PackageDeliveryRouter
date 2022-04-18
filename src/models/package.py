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

    def __repr__(self) -> str:
        return f"ID: {self.package_id}, Address: {self.address}, City: {self.city}, State: {self.state},\n" \
               f"Zipcode: {self.zipcode}, Delivery Deadline: {self.delivery_deadline}, Weight: {self.weight},\n" \
               f"Special Notes: {self.special_notes}"

    def calculate_priority(self) -> int:
        priority: int = 0

        cities = {
            "Salt Lake City": 1,
            "West Valley City": 2,
            "Millcreek": 3,
            "Holladay": 4,
            "Murray": 5
        }
        match self.delivery_deadline:
            case "Delayed on flight---will not arrive to depot until 9:05 am":
                priority += 6
            case "Can only be on truck 2":
                priority += 4
            case "Wrong address listed":
                priority += 7
            case "Must be delivered":
                priority += 4
            case _:
                priority += 5

        return priority + cities[self.city]


def get_deadline(deadline: str) -> Optional[datetime]:
    if deadline == "EOD":
        return None

    temp = re.split("[: ]", deadline)
    if temp[2] == "PM":
        temp[0] += 12

    return datetime(datetime.now().year, datetime.now().month, datetime.now().day, int(temp[0]), int(temp[1]))
