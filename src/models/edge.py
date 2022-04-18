from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from node import Node
    from package import Package


class Edge:
    def __init__(self, node_1: "Node", node_2: "Node", distance: float) -> None:
        self.node_1: Node = node_1
        node_1.add_edge(self)
        self.node_2: Node = node_2
        node_2.add_edge(self)
        self.distance: float = distance
        self.priority: float = 0

    def __repr__(self) -> str:
        return f"{self.distance} miles between {self.node_1.node_name} and {self.node_2.node_name}"

    def __hash__(self):
        return id(self)

    def __eq__(self, other: "Edge"):
        return self.node_1.node_id == other.node_1.node_id and self.node_2.node_id == other.node_2.node_id

    def eligible(self, nodes: list["Node"]) -> bool:
        # Intended to check a group of nodes and see if any of them are present within the current edge to filter
        # out all nodes that aren't needed to be checked for the current trucks route
        return bool(set(nodes) & {self.node_1, self.node_2})

    def calculate_priority(self, packages: list["Package"]) -> None:
        priority: float = self.distance
        for package in packages:
            if package.address == self.node_2.node_address:
                priority += package.priority
        self.priority += priority
