from typing import TYPE_CHECKING, Optional
from .hash_table import HashTable

if TYPE_CHECKING:
    from node import Node
    from edge import Edge


class Graph:
    def __init__(self, nodes=None, edges=None, nodes_list=None, edges_list=None) -> None:
        if nodes is None:
            nodes: HashTable = HashTable()
        if nodes_list is None:
            nodes_list: list["Node"] = []
        if edges is None:
            edges: HashTable = HashTable()
        if edges_list is None:
            edges_list: list["Edge"] = []

        self.nodes: HashTable = nodes
        self.nodes_list: list["Node"] = nodes_list
        self.edges: HashTable = edges
        self.edges_list: list["Edge"] = edges_list

    def add_node(self, node: "Node") -> None:
        self.nodes.insert(node.node_address, node)
        self.nodes_list.append(node)

    def add_edge(self, edge: "Edge") -> None:
        self.edges.insert((edge.origin.node_address, edge.destination.node_address), edge)
        self.edges_list.append(edge)

    def lookup_node(self, address: str) -> Optional["Node"]:
        return self.nodes.lookup(address)

    def lookup_edge(self, origin_address: str, destination_address: str) -> Optional["Edge"]:
        if self.edges.lookup((origin_address, destination_address)):
            return self.edges.lookup((origin_address, destination_address))
        else:
            return self.edges.lookup((destination_address, origin_address))
