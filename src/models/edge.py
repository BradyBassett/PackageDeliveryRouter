from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from node import Node


class Edge:
    def __init__(self, node_1: "Node", node_2: "Node", distance: float) -> None:
        """
        Constructor method for the edge class to initialize the object.\n
        Space-time complexity: O(1)
        """
        self.node_1: Node = node_1
        node_1.add_edge(self)
        self.node_2: Node = node_2
        node_2.add_edge(self)
        self.distance: float = distance
        self.priority: float = 0

    def __repr__(self) -> str:
        """
        Repr method to display the edge class.\n
        Space-time complexity: O(1)
        """
        return f"{self.node_1.node_address} -> {self.distance} -> {self.node_2.node_address}"

    def __lt__(self, other: "Edge"):
        """
        Less than method to compare different edge objects against one another.\n
        Space-time complexity: O(1)
        """
        return self.priority < other.priority

    def eligible(self, nodes: list["Node"]) -> bool:
        """
        This method is provided a list of nodes and determines if the edge is valid based on whether node_1 and
        node_2 of the edge are present within the node list.\n
        Space-time complexity: O(1)
        """
        return bool(set(nodes) & ({self.node_2, self.node_1} | {self.node_1, self.node_2}))

    def calculate_priority(self) -> None:
        """
        Calculates the edge priority based on the sum of node_1 and node_2's priorities with the edges
        distance offset by a product of 10\n
        Space-time complexity: O(1)
        """
        self.priority = self.node_1.priority + self.node_2.priority + (self.distance * 10)
