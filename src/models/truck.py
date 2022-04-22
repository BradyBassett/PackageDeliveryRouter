import sys
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
        self.avg_speed: int = AVG_SPEED
        self.distance_traveled: float = 0.0
        self.current_address: str = "HUB"
        self.delivery_graph: Optional[Graph] = None
        self.delivery_path: list["Edge"] = []

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

    def go_to_next_node(self, current_edge: "Edge") -> list["Package"]:
        if current_edge.origin.node_address == self.current_address:
            self.current_address = current_edge.origin.node_address
        else:
            self.current_address = current_edge.destination.node_address
        self.distance_traveled += current_edge.distance
        return self.deliver_package()

    def deliver_package(self) -> list["Package"]:
        matching_packages: list[Package] = []
        for index, package in enumerate(self.packages):
            if package.address == self.current_address:
                package.delivered_time = self.driver.current_time
                matching_packages.append(self.packages.pop(index))
        return matching_packages
