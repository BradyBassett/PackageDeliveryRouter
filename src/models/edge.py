from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from node import Node


class Edge:
    def __init__(self, origin: "Node", destination: "Node", distance: float) -> None:
        self.destination: Node = destination
        destination.add_edge(self)
        self.origin: Node = origin
        origin.add_edge(self)
        self.distance: float = distance
        self.priority: float = 0

    def __repr__(self) -> str:
        return f"{self.origin.node_address} -> {self.distance} -> {self.destination.node_address}"

    def __lt__(self, other: "Edge"):
        return self.priority < other.priority

    def eligible(self, nodes: list["Node"]) -> bool:
        # Intended to check a group of nodes and see if any of them are present within the current edge to filter
        # out all nodes that aren't needed to be checked for the current trucks route
        return bool(set(nodes) & {self.destination, self.origin})

    def calculate_priority(self) -> None:
        self.priority = self.origin.priority + self.destination.priority + (self.distance * 10)
