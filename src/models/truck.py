import heapq
from typing import TYPE_CHECKING, Optional
from .hash_table import HashTable
from .graph import Graph

if TYPE_CHECKING:
    from driver import Driver
    from package import Package
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
        self.delivery_path: list["Node"] = []
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

    def filter_truck_graph(self, graph: "Graph") -> None:
        package_addresses: list[str] = [p.address for p in self.packages]
        package_nodes: HashTable = HashTable(40)
        nodes_list: list["Node"] = []
        for node in graph.nodes_list:
            address: str = node.node_address
            if address in package_addresses or address == "HUB":
                node.calculate_priority(self.packages)
                node.edges = []
                package_nodes.insert(address, node)
                nodes_list.append(node)

        filtered_edges: HashTable = HashTable(40)
        edges_list: list["Edge"] = []
        for edge in graph.edges_list:
            if edge.eligible(nodes_list):
                edge.origin.edges.append(edge)
                origin: str = edge.origin.node_address
                edge.destination.edges.append(edge)
                destination: str = edge.destination.node_address
                edge.calculate_priority()
                filtered_edges.insert((origin, destination), edge)
                edges_list.append(edge)

        self.delivery_graph = Graph(package_nodes, filtered_edges, nodes_list, edges_list)

    def determine_path(self) -> None:
        start: "Node" = self.find_minimal_spanning_tree()
        self.delivery_path = self.depth_first_search(start, []) + [start]

    def find_minimal_spanning_tree(self) -> "Node":
        """
        O(ElogE)
        """
        num_mst_edges: int = self.delivery_graph.nodes.table_items - 1
        edge_count: int = 0
        # The hub will always be our starting node in this situation
        start: "Node" = self.delivery_graph.lookup_node("HUB")
        curr_node: "Node" = start
        curr_node.visited = True
        pqueue: heapq = []
        _add_edge(curr_node, pqueue)

        while pqueue and edge_count != num_mst_edges:
            prev_node: "Node" = curr_node
            edge = heapq.heappop(pqueue)

            if curr_node == edge.origin:
                curr_node = edge.destination
            else:
                curr_node = edge.origin

            if curr_node.visited:
                continue

            curr_node.visited = True
            curr_node.parent_distance = edge.distance
            prev_node.children.append(curr_node)

            _add_edge(curr_node, pqueue)

        return start

    def depth_first_search(self, node: "Node", path: list["Node"]) -> list["Node"]:
        """
        O(E + N)
        """
        if node in path:
            return path

        for package in self.packages:
            if package.address == node.node_address or package.address == "HUB":
                path.append(node)
                break

        for child in node.children:
            path = self.depth_first_search(child, path)

        return path

    def go_to_next_node(self) -> None:
        self.current_address = self.delivery_path.pop(0).node_address
        distance: float = self.delivery_graph.lookup_node(self.current_address).parent_distance
        self.distance_traveled += distance
        self.driver.progress_time(distance, AVG_SPEED)

    def deliver_package(self) -> int:
        matching_packages: list["Package"] = []
        for package in self.packages:
            if package.address == self.current_address:
                package.delivered_time = self.driver.current_time
                matching_packages.append(package)

        for package in matching_packages:
            self.packages.remove(package)

        return len(matching_packages)


def _add_edge(curr_node: "Node", pqueue: heapq):
    for edge in curr_node.edges:
        if (edge.origin == curr_node and edge.destination.visited is False) or \
                (edge.destination == curr_node and edge.origin.visited is False):
            heapq.heappush(pqueue, edge)