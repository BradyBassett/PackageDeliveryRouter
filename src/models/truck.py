import math
import sys
from datetime import timedelta
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from driver import Driver
    from package import Package
    from graph import Graph
    from node import Node
    from edge import Edge

MAX_CAPACITY: int = 16
AVG_SPEED: int = 18  # MPH


class Truck:
    def __init__(self, truck_id: int) -> None:
        self.truck_id: int = truck_id
        self.driver: Optional[Driver] = None
        self.capacity: int = MAX_CAPACITY
        self.packages: list[Package] = []
        self.distance_traveled: float = 0.0
        self.current_address: str = "HUB"
        self.delivery_graph: Optional[Graph] = None
        self.delivery_path: list["Edge"] = []
        self.returned: bool = True

    def __repr__(self) -> str:
        return f"Truck ID: {self.truck_id}, Current Driver: {self.driver.driver_id}, Packages Loaded: {self.packages}"

    def load_package(self, package: "Package") -> None:
        self.packages.append(package)

    def get_total_packages(self) -> int:
        return len(self.packages)

    def get_max_priority(self) -> str:
        max_priority: int = -1
        result: str = ""
        for package in self.packages:
            if max_priority <= package.priority:
                max_priority = package.priority
                result = package.address
        return result

    def determine_path(self) -> None:
        hub: "Node" = self.delivery_graph.nodes.remove("HUB")

        curr_node: "Node" = hub
        path: list["Edge"] = []
        while self.delivery_graph.nodes.table_items:
            min_priority: tuple[str, float] = ("", sys.maxsize)
            min_edge: Optional["Edge"] = None
            for edge in curr_node.edges:
                if self.delivery_graph.lookup_node(edge.destination.node_address):
                    if edge.priority < min_priority[1]:
                        min_priority = (edge.destination.node_address, edge.priority)
                        min_edge = edge
                elif self.delivery_graph.lookup_node(edge.origin.node_address):
                    if edge.priority < min_priority[1]:
                        min_priority = (edge.origin.node_address, edge.priority)
                        min_edge = edge
            curr_node = self.delivery_graph.nodes.remove(min_priority[0])
            path.append(min_edge)
        path.append(curr_node.edges[0])
        self.delivery_path = path

    def go_to_next_node(self, current_edge: "Edge") -> None:
        if current_edge.origin.node_address == self.current_address:
            self.current_address = current_edge.destination.node_address
        else:
            self.current_address = current_edge.origin.node_address
        self.distance_traveled += current_edge.distance

        travel_time: float = current_edge.distance / AVG_SPEED
        travel_time_hour: int = int(travel_time)
        travel_time_minute: int = int(travel_time * 60 - (travel_time_hour * 60))
        travel_time_second: int = \
            int(travel_time * math.pow(60, 2) - (travel_time_minute * 60) - (travel_time_hour * 60))
        self.driver.current_time += timedelta(
            hours=travel_time_hour,
            minutes=travel_time_minute,
            seconds=travel_time_second
        )

    def deliver_package(self) -> int:
        matching_packages: list["Package"] = []
        for package in self.packages:
            if package.address == self.current_address:
                package.delivered_time = self.driver.current_time
                matching_packages.append(package)

        for package in matching_packages:
            self.packages.remove(package)

        return len(matching_packages)