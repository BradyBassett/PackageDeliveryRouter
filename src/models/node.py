from typing import TYPE_CHECKING
import sys
if TYPE_CHECKING:
    from edge import Edge


class Node:
    def __init__(self, node_id: int, node_name: str, node_address: str, node_zipcode: str) -> None:
        self.node_id: int = node_id
        self.node_name: str = node_name
        self.node_address: str = node_address
        self.node_zipcode: str = node_zipcode
        self.edges: list["Edge"] = []
        self.cost: float = sys.maxsize
        self.prev_node: list[Node] = []

    def __repr__(self) -> str:
        return f"ID: {self.node_id}, Name: {self.node_name}, Address: {self.node_address}, ZipCode: " \
               f"{self.node_zipcode},\nEdge Ids: {self.edges}"

    def __hash__(self):
        return id(self)

    def __eq__(self, other: "Node"):
        return self.node_id == other.node_id

    def __lt__(self, other: "Node"):
        return self.cost < other.cost

    def add_edge(self, edge: "Edge") -> None:
        self.edges.append(edge)
