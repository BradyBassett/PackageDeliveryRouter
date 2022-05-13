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
        """
        Constructor for the truck class to initialize a truck object.\n
        Space complexity: O(N + M)\n
        Time complexity: O(1)
        """
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
        """
        Repr function to display the truck object.\n
        Space-time complexity: O(1)
        """
        return f"Truck ID: {self.truck_id}, Current Driver: {self.driver.driver_id}, Packages Loaded: {self.packages}"

    def load_package(self, package: "Package") -> None:
        """
        Method to load a package onto the truck.\n
        Space-time complexity: O(1)
        """
        self.packages.append(package)

    def filter_truck_graph(self, graph: "Graph") -> None:
        """
        This method when provided a graph parameter will filter out all edges and nodes that do not match the trucks
        package list.\n
        Space-time complexity: O(P + N + E)
        """
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
                edge.node_1.edges.append(edge)
                node_1: str = edge.node_1.node_address
                edge.node_2.edges.append(edge)
                node_2: str = edge.node_2.node_address
                edge.calculate_priority()
                filtered_edges.insert((node_1, node_2), edge)
                edges_list.append(edge)

        self.delivery_graph = Graph(package_nodes, filtered_edges, nodes_list, edges_list)

    def determine_path(self) -> None:
        """
        This function is a helper function to determine the trucks path based on the mst-dfs algorithms\n
        Space-time complexity: O(1)
        """
        start: "Node" = self.find_minimal_spanning_tree()
        self.delivery_path = self.depth_first_search(start, []) + [start]

    def find_minimal_spanning_tree(self) -> "Node":
        """
        This method implements prims algorithm to generate a minimal spanning tree starting from to hub node.
        Space complexity: O(N)\n
        Time complexity: O(ElogE)
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

            if curr_node == edge.node_1:
                curr_node = edge.node_2
            else:
                curr_node = edge.node_1

            if curr_node.visited:
                continue

            curr_node.visited = True
            curr_node.parent_distance = edge.distance
            prev_node.children.append(curr_node)

            _add_edge(curr_node, pqueue)

        return start

    def depth_first_search(self, node: "Node", path: list["Node"]) -> list["Node"]:
        """
        This method implements the depth first search algorithm to traverse the nodes in the given mst and return the
        path taken, ignoring all duplicate nodes\n
        Space Complexity: O(N)\n
        Time complexity: O(N + P + C))
        """
        if node in path:
            return path

        # Filters out every other node that is not applicable to the packages
        for package in self.packages:
            if package.address == node.node_address or package.address == "HUB":
                path.append(node)
                break

        for child in node.children:
            path = self.depth_first_search(child, path)

        return path

    def go_to_next_node(self) -> None:
        """
        Using the trucks' delivery path this function progresses the truck to the next available node and progresses the
        drivers time using the distance between the two nodes, as well as adding to the total distance traveled.\n
        Space-time complexity: O(1)
        """
        self.current_address = self.delivery_path.pop(0).node_address
        distance: float = self.delivery_graph.lookup_node(self.current_address).parent_distance
        self.distance_traveled += distance
        self.driver.progress_time(distance, AVG_SPEED)

    def deliver_package(self) -> int:
        """
        This function loops through each package and for each package whose delivery address matches the trucks current
        address will deliver that package.\n
        Space complexity: O(M)\n
        Time complexity: O(P + M)
        """
        # Matching packages is used to be able to safely remove the packages without interfering with the package loop
        matching_packages: list["Package"] = []
        for package in self.packages:
            if package.address == self.current_address:
                package.delivered_time = self.driver.current_time
                matching_packages.append(package)

        for package in matching_packages:
            self.packages.remove(package)

        return len(matching_packages)


def _add_edge(curr_node: "Node", pqueue: heapq):
    """
    Adds the first applicable edge from the given node to the priority queue.
    Space complexity: O(1)
    Time complexity: O(N)
    """
    for edge in curr_node.edges:
        if (edge.node_1 == curr_node and edge.node_2.visited is False) or \
                (edge.node_2 == curr_node and edge.node_1.visited is False):
            heapq.heappush(pqueue, edge)
