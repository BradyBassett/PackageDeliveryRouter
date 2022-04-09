from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from driver import Driver
    from package import Package

MAX_CAPACITY: int = 16
AVG_SPEED: int = 18


class Truck:
    def __init__(self, truck_id: int) -> None:
        self.truck_id: int = truck_id
        self.driver: Optional["Driver"] = None
        self.capacity: int = MAX_CAPACITY
        self.packages: list["Package"] = []
        self.avg_speed: int = AVG_SPEED  # MPH
        self.distance_traveled: float = 0.0

    def __repr__(self) -> str:
        return f"Truck ID: {self.truck_id}, Current Driver: {self.driver.driver_id}, Packages Loaded: {self.packages}"
