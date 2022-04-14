from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from node import Node


class Edge:
    def __init__(self, node_1: "Node", node_2: "Node", distance: float) -> None:
        self.node_1: "Node" = node_1
        node_1.add_edge(self)
        self.node_2: "Node" = node_2
        node_2.add_edge(self)
        self.distance: float = distance

    def __repr__(self) -> str:
        return f"{self.distance} miles between {self.node_1.node_name} and {self.node_2.node_name}"

    def eligible(self, nodes: list["Node"]) -> bool:
        # Intended to check a group of nodes and see if any of them are present within the current edge to filter
        # out all nodes that aren't needed to be checked for the current trucks route
        return bool(set(nodes) & {self.node_1, self.node_2})
