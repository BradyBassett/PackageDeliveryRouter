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
        self.current_address: str = "HUB"

    def __repr__(self) -> str:
        return f"Truck ID: {self.truck_id}, Current Driver: {self.driver.driver_id}, Packages Loaded: {self.packages}"

    def load_package(self, package: "Package") -> None:
        self.packages.append(package)

    def get_total_packages(self) -> int:
        return len(self.packages)

    def go_to_next_node(self, next_node_address: str):
        self.current_address = next_node_address
        self.deliver_package()

    def deliver_package(self) -> list["Package"]:
        matching_packages: list["Package"] = []
        for index, package in enumerate(self.packages):
            if package.address == self.current_address:
                matching_packages.append(self.packages.pop(index))
        return matching_packages
