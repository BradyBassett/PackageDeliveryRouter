from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from node import Node
    from edge import Edge


class Graph:
    def __init__(self) -> None:
        self.nodes: list["Node"] = []
        self.edges: list["Edge"] = []

    def add_node(self, node: "Node") -> None:
        self.nodes.append(node)

    def add_edge(self, edge: "Edge") -> None:
        self.edges.append(edge)

    def get_edges(self, node: "Node") -> list["Edge"]:
        return node.edges

    def get_node_by_address(self, address: str) -> Optional["Node"]:
        for node in self.nodes:
            if node.node_address == address:
                return node

    def get_edge_by_addresses(self, address_1: str, address_2: str) -> Optional["Edge"]:
        for edge in self.edges:
            if edge.node_1 == address_1 and edge.node_2 == address_2:
                return edge

    def get_closest_node(self, node: "Node") -> "Node":
        edges: list["Edge"] = self.get_edges(node)
        edges.sort(key=lambda edge: edge.distance)
        return edges[0].node_2 if node == edges[0].node_1 else edges[0].node_1
