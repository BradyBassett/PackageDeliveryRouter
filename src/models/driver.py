from typing import TYPE_CHECKING, Optional
from datetime import datetime

if TYPE_CHECKING:
    from truck import Truck


START_HOUR: int = 8


class Driver:
    def __init__(self, driver_id: int) -> None:
        self.driver_id: int = driver_id
        self.current_truck: Optional[Truck] = None
        self.current_time: datetime = datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                                               START_HOUR)

    def __repr__(self) -> str:
        return f"Driver ID: {self.driver_id}, Current Truck: {self.current_truck.truck_id}"

    def select_truck(self, trucks: list["Truck"]):
        for truck in trucks:
            if truck.driver is None:
                self.current_truck = truck
                truck.driver = self
                break
