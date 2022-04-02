"""
First
Last
ID
"""
from csv import reader
from models.package import Package
from models.hash_table import HashTable
from models.graph import Graph
from models.edge import Edge
from models.node import Node


class Application:
    def __init__(self) -> None:
        self.packages: HashTable = HashTable()
        self.graph: Graph = Graph()

    def start(self) -> None:
        self.load_packages()
        self.load_distances()
        print(self.graph.nodes[2])

    def load_packages(self) -> None:
        with open("data/packages.csv") as file:
            file_data: reader = reader(file)
            for row in file_data:
                package: Package = Package(int(row[0]), row[1], row[2], row[3],
                                           int(row[4]), row[5], int(row[6]), row[7])
                self.packages.insert(package.package_id, package)

    def load_distances(self) -> None:
        with open("data/addresses.csv") as file:
            file_data: reader = reader(file)
            for row in file_data:
                self.graph.add_node(Node(int(row[0]), row[1], row[2], row[3]))

        with open("data/distances.csv") as file:
            file_data: reader = reader(file)
            for i, row in enumerate(file_data):
                for j in range(i):
                    if i is not j:
                        node_1: "Node" = self.graph.nodes[i]
                        node_2: "Node" = self.graph.nodes[j]
                        self.graph.add_edge(Edge(node_1, node_2, row[j]))


def main() -> None:
    Application().start()


if __name__ == "__main__":
    main()
