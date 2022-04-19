import sys
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from driver import Driver
    from package import Package
    from graph import Graph
    from node import Node
    from edge import Edge

MAX_CAPACITY: int = 16
AVG_SPEED: int = 18


class Truck:
    def __init__(self, truck_id: int) -> None:
        self.truck_id: int = truck_id
        self.driver: Optional[Driver] = None
        self.capacity: int = MAX_CAPACITY
        self.packages: list[Package] = []
        self.avg_speed: int = AVG_SPEED  # MPH
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

    def determine_path(self):
        curr_node: "Node" = self.delivery_graph.nodes.remove("HUB")
        visited: list["Node"] = [curr_node]
        while self.delivery_graph.nodes.table_items:
            min_priority: tuple[str, float] = ("", sys.maxsize)
            for edge in curr_node.edges:
                if self.delivery_graph.lookup_node(edge.destination.node_address):
                    if edge.priority < min_priority[1]:
                        min_priority = (edge.destination.node_address, edge.priority)
                elif self.delivery_graph.lookup_node(edge.origin.node_address):
                    if edge.priority < min_priority[1]:
                        min_priority = (edge.origin.node_address, edge.priority)
            curr_node = self.delivery_graph.nodes.remove(min_priority[0])
            visited.append(curr_node)

        return visited

    def go_to_next_node(self, next_node_address: str) -> None:
        self.current_address = next_node_address
        self.deliver_package()

    def deliver_package(self) -> list["Package"]:
        matching_packages: list[Package] = []
        for index, package in enumerate(self.packages):
            if package.address == self.current_address:
                matching_packages.append(self.packages.pop(index))
        return matching_packages
