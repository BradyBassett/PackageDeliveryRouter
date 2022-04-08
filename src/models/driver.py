from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from truck import Truck


class Driver:
    def __init__(self, driver_id: int) -> None:
        self.driver_id: int = driver_id
        self.current_truck: Optional["Truck"] = None

    def __repr__(self) -> str:
        return f"Driver ID: {self.driver_id}, Current Truck: {self.current_truck.truck_id}"
