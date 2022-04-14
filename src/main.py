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
from models.heap import Heap
from models.truck import Truck
from models.driver import Driver

NUMBER_OF_TRUCKS: int = 3
NUMBER_OF_DRIVERS: int = 2


class Application:
    def __init__(self) -> None:
        self.packages: "HashTable" = HashTable()
        self.graph: "Graph" = Graph()
        self.heap: "Heap" = Heap()
        self.trucks: list["Truck"] = [Truck(i + 1) for i in range(NUMBER_OF_TRUCKS)]
        self.drivers: list["Driver"] = [Driver(i + 1) for i in range(NUMBER_OF_DRIVERS)]

    def start(self) -> None:
        self.load_packages()
        self.load_trucks()
        self.load_distances()

    def load_packages(self) -> None:
        with open("data/packages.csv") as file:
            file_data: reader = reader(file)
            for row in file_data:
                package: Package = Package(int(row[0]), row[1], row[2], row[3],
                                           int(row[4]), row[5], int(row[6]), row[7])
                self.packages.insert(package.package_id, package)

    def load_trucks(self):
        # TODO - eventually calculate more optimal truck loading based on special notes
        truck_index = 0
        for i in range(self.packages.table_items):
            self.trucks[truck_index].load_package(self.packages.lookup(i + 1))
            if self.trucks[truck_index].get_total_packages() == self.trucks[truck_index].capacity:
                truck_index += 1

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

    def record_deliveries(self, index: int) -> None:
        package_addresses: list[str] = [p.address for p in self.trucks[index].packages]
        package_nodes: list["Node"] = [n for n in self.graph.nodes if n.node_address in package_addresses]
        edges_filter: filter = filter(lambda x: x.eligible(package_nodes), self.graph.edges)
        # TODO - get a sorted list of nodes to deliver to based on some weight value
        # sorted_edges: list["Edge"] = sorted(edges_filter, key=lambda x: x.distance)


def main() -> None:
    Application().start()


if __name__ == "__main__":
    main()
