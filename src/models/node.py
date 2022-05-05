from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from edge import Edge
    from package import Package


class Node:
    def __init__(self, node_id: int, node_name: str, node_address: str, node_zipcode: str) -> None:
        self.node_id: int = node_id
        self.node_name: str = node_name
        self.node_address: str = node_address
        self.node_zipcode: str = node_zipcode
        self.edges: list["Edge"] = []
        self.priority: float = 0
        self.children: list["Node"] = []
        self.parent_distance: int = 0
        self.visited: bool = False

    def __repr__(self) -> str:
        return f"{self.node_id}, {self.node_name}"

    def add_edge(self, edge: "Edge") -> None:
        self.edges.append(edge)

    def calculate_priority(self, packages: list["Package"]) -> None:
        for package in packages:
            if package.address == self.node_address:
                self.priority += package.priority
