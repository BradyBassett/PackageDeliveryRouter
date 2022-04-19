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
from models.truck import Truck
from models.driver import Driver

NUMBER_OF_TRUCKS: int = 3
NUMBER_OF_DRIVERS: int = 2


class Application:
    def __init__(self) -> None:
        self.packages: HashTable = HashTable()
        self.graph: Graph = Graph()
        self.nodes: list["Node"] = []
        self.edges: list["Edge"] = []
        self.trucks: list[Truck] = [Truck(i + 1) for i in range(NUMBER_OF_TRUCKS)]
        self.drivers: list[Driver] = [Driver(i + 1) for i in range(NUMBER_OF_DRIVERS)]

    def start(self) -> None:
        self.load_packages()
        self.load_trucks()
        self.load_distances()
        for i in range(len(self.trucks)):
            self.trucks[i].delivery_graph = self.filter_truck_graph(i)
            self.trucks[i].delivery_graph = self.filter_truck_graph(i)

    def load_packages(self) -> None:
        with open("data/packages.csv") as file:
            file_data: reader = reader(file)
            for row in file_data:
                package: Package = Package(int(row[0]), row[1], row[2], row[3],
                                           int(row[4]), row[5], int(row[6]), row[7])
                self.packages.insert(package.package_id, package)

    def load_trucks(self) -> None:
        truck_index = 0
        for i in range(self.packages.table_items):
            package: "Package" = self.packages.lookup(i + 1)
            if package.special_notes == "Can only be on truck 2":
                self.trucks[1].load_package(package)
                continue
            elif package.special_notes == "Wrong address listed" or package.special_notes == "Delayed on " \
                                                                                             "flight---will not " \
                                                                                             "arrive to depot until " \
                                                                                             "9:05 am" or "Must be " \
                                                                                                          "delivered " \
                                                                                                          "with" in \
                    package.special_notes:
                self.trucks[2].load_package(package)
            else:
                self.trucks[truck_index].load_package(package)

            if self.trucks[truck_index].get_total_packages() == self.trucks[truck_index].capacity:
                truck_index += 1

    def load_distances(self) -> None:
        with open("data/addresses.csv") as file:
            file_data: reader = reader(file)
            for row in file_data:
                node: "Node" = Node(int(row[0]), row[1], row[2], row[3])
                self.graph.add_node(node)
                self.nodes.append(node)

        with open("data/distances.csv") as file:
            file_data: reader = reader(file)
            for i, row in enumerate(file_data):
                for j in range(i):
                    if i is not j:
                        edge: "Edge" = Edge(self.nodes[j], self.nodes[i], float(row[j]))
                        self.graph.add_edge(edge)
                        self.edges.append(edge)

    def filter_truck_graph(self, index: int) -> Graph:
        package_addresses: list[str] = [p.address for p in self.trucks[index].packages]
        package_nodes: HashTable = HashTable(40)
        temp_nodes: list["Node"] = []
        i = 1
        for node in self.nodes:
            address: str = node.node_address
            if address in package_addresses or address == "HUB":
                package_nodes.insert(address, node)
                i += 1
                temp_nodes.append(node)

        filtered_edges: HashTable = HashTable()
        for edge in self.edges:
            if edge.eligible(temp_nodes):
                origin: str = edge.origin.node_address
                destination: str = edge.destination.node_address
                edge.calculate_priority(self.trucks[index].packages)
                filtered_edges.insert((origin, destination), edge)

        return Graph(package_nodes, filtered_edges)


def main() -> None:
    Application().start()


if __name__ == "__main__":
    main()
