from typing import TYPE_CHECKING
from .hash_table import HashTable
if TYPE_CHECKING:
    from node import Node
    from edge import Edge


def get_closest_node(node: "Node") -> "Node":
    edges: list[Edge] = node.edges
    edges.sort(key=lambda edge: edge.distance)
    return edges[0].origin if node == edges[0].destination else edges[0].destination


class Graph:
    def __init__(self, nodes=None, edges=None) -> None:
        if nodes is None:
            nodes: HashTable = HashTable()
        if edges is None:
            edges: HashTable = HashTable()

        self.nodes: HashTable = nodes
        self.edges: HashTable = edges

    def add_node(self, node: "Node") -> None:
        self.nodes.insert(node.node_address, node)

    def add_edge(self, edge: "Edge") -> None:
        self.edges.insert((edge.origin.node_address, edge.destination.node_address), edge)

    def lookup_node(self, address: str):
        return self.nodes.lookup(address)

    def lookup_edge(self, origin_address: str, destination_address: str):
        if self.edges.lookup((origin_address, destination_address)):
            return self.edges.lookup((origin_address, destination_address))
        else:
            return self.edges.lookup((destination_address, origin_address))
