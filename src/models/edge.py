from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from node import Node


class Edge:
    def __init__(self, origin: "Node", destination: "Node", distance: float) -> None:
        """
        Constructor method for the edge class to initialize the object.
        Space-time complexity: O(1)
        """
        self.destination: Node = destination
        destination.add_edge(self)
        self.origin: Node = origin
        origin.add_edge(self)
        self.distance: float = distance
        self.priority: float = 0

    def __repr__(self) -> str:
        """
        Repr method to display the edge class.
        Space-time complexity: O(1)
        """
        return f"{self.origin.node_address} -> {self.distance} -> {self.destination.node_address}"

    def __lt__(self, other: "Edge"):
        """
        Less than method to compare different edge objects against one another.
        Space-time complexity: O(1)
        """
        return self.priority < other.priority

    def eligible(self, nodes: list["Node"]) -> bool:
        """
        This method is provided a list of nodes and determines if the edge is valid based on whether the origin and
        destination nodes of the edge are present within the node list.
        Space-time complexity: O(1)
        """
        # Intended to check a group of nodes and see if any of them are present within the current edge to filter
        # out all nodes that aren't needed to be checked for the current trucks route
        return bool(set(nodes) & ({self.destination, self.origin} | {self.origin, self.destination}))

    def calculate_priority(self) -> None:
        """
        Calculates the edge priority based on the sum of the origin node and destination nodes priorities with the edges
        distance offset by a product of 10
        Space-time complexity: O(1)
        """
        self.priority = self.origin.priority + self.destination.priority + (self.distance * 10)
