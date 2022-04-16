from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from node import Node
    from edge import Edge


def get_closest_node(node: "Node") -> "Node":
    edges: list[Edge] = node.edges
    edges.sort(key=lambda edge: edge.distance)
    return edges[0].node_2 if node == edges[0].node_1 else edges[0].node_1


class Graph:
    def __init__(self, nodes=None, edges=None) -> None:
        if nodes is None:
            nodes = []
        if edges is None:
            edges = []

        self.nodes: list[Node] = nodes
        self.edges: list[Edge] = edges

    def add_node(self, node: "Node") -> None:
        self.nodes.append(node)

    def pop_node(self, node: "Node") -> Optional["Node"]:
        for index, arr_node in enumerate(self.nodes):
            if arr_node == node:
                return self.nodes.pop(index)

    def pop_edge(self, edge: "Edge") -> Optional["Edge"]:
        for index, arr_edge in enumerate(self.edges):
            if arr_edge == edge:
                return self.edges.pop(index)

    def add_edge(self, edge: "Edge") -> None:
        self.edges.append(edge)

    def get_node_by_address(self, address: str) -> Optional["Node"]:
        for node in self.nodes:
            if node.node_address == address:
                return node

    def get_edge_by_addresses(self, address_1: str, address_2: str) -> Optional["Edge"]:
        for edge in self.edges:
            if edge.node_1 == address_1 and edge.node_2 == address_2:
                return edge
