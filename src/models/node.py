from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from edge import Edge
    from package import Package


class Node:
    def __init__(self, node_id: int, node_name: str, node_address: str, node_zipcode: str) -> None:
        """
        Constructor method for initializing a new node object.\n
        Space complexity: O(N + M)\n
        Time complexity: O(1)
        """
        self.node_id: int = node_id
        self.node_name: str = node_name
        self.node_address: str = node_address
        self.node_zipcode: str = node_zipcode
        self.edges: list["Edge"] = []
        self.priority: float = 0
        self.children: list["Node"] = []
        self.parent_distance: int = 0
        self.visited: bool = False

    def __repr__(self) -> str:
        """
        Repr method to display a node object\n
        Space-time complexity: O(1)
        """
        return f"{self.node_id}, {self.node_name}"

    def add_edge(self, edge: "Edge") -> None:
        """
        Method that appends a new edge to the nods edges list\n
        Space-time complexity: O(1)
        """
        self.edges.append(edge)

    def calculate_priority(self, packages: list["Package"]) -> None:
        """
        Given a list of packages calculate the nodes priority based on the sum of all package priorities that match the
        nodes address.\n
        Space complexity: O(1)\n
        Time complexity: O(N)
        """
        for package in packages:
            if package.address == self.node_address:
                self.priority += package.priority
