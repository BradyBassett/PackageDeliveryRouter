from typing import TYPE_CHECKING, Optional
import sys
import heapq

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
        self.driver: Optional["Driver"] = None
        self.capacity: int = MAX_CAPACITY
        self.packages: list["Package"] = []
        self.avg_speed: int = AVG_SPEED  # MPH
        self.distance_traveled: float = 0.0
        self.current_address: str = "HUB"
        self.delivery_graph: Optional["Graph"] = None

    def __repr__(self) -> str:
        return f"Truck ID: {self.truck_id}, Current Driver: {self.driver.driver_id}, Packages Loaded: {self.packages}"

    def load_package(self, package: "Package") -> None:
        self.packages.append(package)

    def get_total_packages(self) -> int:
        return len(self.packages)

    def determine_path(self, src: str, dest: str) -> list["Node"]:
        for node in self.delivery_graph.nodes:
            node.cost = sys.maxsize
            node.prev_node = []

        self.delivery_graph.get_node_by_address(src).cost = 0
        visited: list["Node"] = []
        curr_node: "Node" = self.delivery_graph.get_node_by_address(src)

        for i in range(len(self.delivery_graph.nodes) - 1):
            if curr_node not in visited:
                visited.append(curr_node)
                min_heap: heapq = []
                edges: list["Edge"] = self.delivery_graph.get_node_by_address(curr_node.node_address).edges
                for edge in edges:
                    if edge.node_2 not in visited:
                        cost = curr_node.cost + edge.node_2.cost
                        if cost < edge.node_2.cost:
                            edge.node_2.cost = cost
                            edge.node_2.prev_node = curr_node.prev_node + [curr_node]
                        heapq.heappush(min_heap, [edge.node_1.cost, edge.node_2])
                heapq.heapify(min_heap)
                curr_node = min_heap[0][1]

        return self.delivery_graph.get_node_by_address(dest).prev_node + [self.delivery_graph.get_node_by_address(dest)]

    def go_to_next_node(self, next_node_address: str) -> None:
        self.current_address = next_node_address
        self.deliver_package()

    def deliver_package(self) -> list["Package"]:
        matching_packages: list["Package"] = []
        for index, package in enumerate(self.packages):
            if package.address == self.current_address:
                matching_packages.append(self.packages.pop(index))
        return matching_packages
