from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from edge import Edge


class Node:
    def __init__(self, node_id: int, node_name: str, node_address: str, node_zipcode: str):
        self.node_id: int = node_id
        self.node_name: str = node_name
        self.node_address: str = node_address
        self.node_zipcode: str = node_zipcode
        self.edges: list["Edge"] = []

    def __repr__(self) -> str:
        return f"ID: {self.node_id}, Name: {self.node_name}, Address: {self.node_address}, ZipCode: " \
               f"{self.node_zipcode},\nEdge Ids: {self.edges}"

    def add_edge(self, edge: "Edge"):
        self.edges.append(edge)
