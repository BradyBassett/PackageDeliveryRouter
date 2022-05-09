from typing import TYPE_CHECKING, Optional
from .hash_table import HashTable

if TYPE_CHECKING:
    from node import Node
    from edge import Edge


class Graph:
    def __init__(self, nodes=None, edges=None, nodes_list=None, edges_list=None) -> None:
        """
        Constructor method to initialize a graph object.\n
        Space complexity: O(N + M)\n
        Time complexity: O(1)
        """
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
        """
        Method to add a node to the nodes hash table as well as the nodes_list list.\n
        Space-time complexity: O(1)
        """
        self.nodes.insert(node.node_address, node)
        self.nodes_list.append(node)

    def add_edge(self, edge: "Edge") -> None:
        """
        Method to add an edge to the edges hash table as well as the edges_list list.\n
        Space-time complexity: O(1)
        """
        self.edges.insert((edge.node_1.node_address, edge.node_2.node_address), edge)
        self.edges_list.append(edge)

    def lookup_node(self, address: str) -> Optional["Node"]:
        """
        A method to lookup whether a node is present within the graph using a provided address.\n
        Space-time complexity: O(1)
        """
        return self.nodes.lookup(address)

    def lookup_edge(self, node_1_address: str, node_2_address: str) -> Optional["Edge"]:
        """
        A method to lookup whether an edge is present within the graph using a provided node_1 and node_2
        address.\n
        Space-time complexity: O(1)
        """
        if self.edges.lookup((node_1_address, node_2_address)):
            return self.edges.lookup((node_1_address, node_2_address))
        else:
            return self.edges.lookup((node_2_address, node_1_address))
