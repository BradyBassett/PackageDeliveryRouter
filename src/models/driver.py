from typing import TYPE_CHECKING, Optional
import math
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from truck import Truck


START_HOUR: int = 8


class Driver:
    def __init__(self, driver_id: int) -> None:
        self.driver_id: int = driver_id
        self.current_truck: Optional[Truck] = None
        self.current_time: datetime = datetime.now().replace(hour=START_HOUR, minute=0, second=0, microsecond=0)

    def __repr__(self) -> str:
        return f"Driver ID: {self.driver_id}, Current Truck: {self.current_truck.truck_id}"

    def select_truck(self, trucks: list["Truck"]) -> None:
        for truck in trucks:
            if truck.driver is None and truck.returned is True:
                self.current_truck = truck
                truck.driver = self
                break

    def progress_time(self, distance: float, avg_speed: int):
        travel_time: float = distance / avg_speed
        travel_time_hour: int = int(travel_time)
        travel_time_minute: int = int(travel_time * 60 - (travel_time_hour * 60))
        travel_time_second: int = \
            int(travel_time * math.pow(60, 2) - (travel_time_minute * 60) - (travel_time_hour * 60))
        self.current_time += timedelta(
            hours=travel_time_hour,
            minutes=travel_time_minute,
            seconds=travel_time_second
        )
