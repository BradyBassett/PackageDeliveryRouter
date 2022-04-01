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
