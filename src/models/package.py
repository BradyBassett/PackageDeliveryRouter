from datetime import datetime
import re


class Package:
    def __init__(self, package_id: int, address: str, city: str, state: str, zipcode: int, deadline: str, weight: int,
                 special_notes: str) -> None:
        self.package_id: int = package_id
        self.address: str = address
        self.city: str = city
        self.state: str = state
        self.zipcode: int = zipcode
        self.delivery_deadline: datetime = get_deadline(deadline)
        self.weight: int = weight
        self.special_notes: str = special_notes

    def __repr__(self) -> str:
        return f"ID: {self.package_id}, Address: {self.address}, City: {self.city}, State: {self.state},\n" \
               f"Zipcode: {self.zipcode}, Delivery Deadline: {self.delivery_deadline}, Weight: {self.weight},\n" \
               f"Special Notes: {self.special_notes}"

    def calculate_priority(self):
        pass


def get_deadline(deadline: str) -> datetime:
    if deadline == "EOD":
        return datetime.now()

    temp = re.split("[: ]", deadline)
    if temp[2] == "PM":
        temp[0] += 12

    return datetime(datetime.now().year, datetime.now().month, datetime.now().day, int(temp[0]), int(temp[1]))
