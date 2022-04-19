from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from node import Node
    from package import Package


class Edge:
    def __init__(self, origin: "Node", destination: "Node", distance: float) -> None:
        self.destination: Node = destination
        destination.add_edge(self)
        self.origin: Node = origin
        origin.add_edge(self)
        self.distance: float = distance
        self.priority: float = 0

    def __repr__(self) -> str:
        return f"{self.origin.node_name} -> {self.distance} -> {self.destination.node_name}"

    def __hash__(self):
        return id(self)

    def __eq__(self, other: "Edge"):
        return self.destination.node_id == other.destination.node_id and self.origin.node_id == other.origin.node_id

    def eligible(self, nodes: list["Node"]) -> bool:
        # Intended to check a group of nodes and see if any of them are present within the current edge to filter
        # out all nodes that aren't needed to be checked for the current trucks route
        return bool(set(nodes) & {self.destination, self.origin})

    def calculate_priority(self, packages: list["Package"]) -> None:
        priority: float = self.distance
        for package in packages:
            if package.address == self.origin.node_address:
                priority += package.priority
        self.priority += priority
