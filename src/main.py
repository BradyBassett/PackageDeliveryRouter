"""
First
Last
ID
"""
from datetime import datetime
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
FLIGHT_ARRIVED: datetime = datetime.now().replace(hour=9, minute=5)
PACKAGE_ADDRESS_CORRECTED: datetime = datetime.now().replace(hour=10, minute=20)
INFO_UPDATE_HOUR: int = 10
INFO_UPDATE_MINUTE: int = 20
CORRECT_PACKAGE_ADDRESS: str = "410 South State St"
CORRECT_PACKAGE_ZIP: int = 84111


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
        for truck in self.trucks:
            truck.delivery_graph = self.filter_truck_graph(truck)
            truck.determine_path()
            print(truck.delivery_path)
            print(truck.packages, "\n")
        self.deliver_packages()
        self.cli()

    def load_packages(self) -> None:
        with open("data/packages.csv") as file:
            file_data: reader = reader(file)
            for row in file_data:
                package: Package = Package(int(row[0]), row[1], row[2], row[3],
                                           int(row[4]), row[5], int(row[6]), row[7])
                self.packages.insert(package.package_id, package)

    def load_trucks(self) -> None:
        packages: list["Package"] = []
        pre_loaded_packages: list[int] = [3, 18, 36, 38]

        for i in range(self.packages.table_items):
            package: "Package" = self.packages.lookup(i + 1)
            if package.package_id not in pre_loaded_packages:
                packages.append(package)

        for package_id in pre_loaded_packages:
            self.trucks[1].load_package(self.packages.lookup(package_id))

        packages.sort(key=lambda x: x.priority)
        truck_index: int = 0
        for package in packages:
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

    def filter_truck_graph(self, truck: "Truck") -> Graph:
        package_addresses: list[str] = [p.address for p in truck.packages]
        package_nodes: HashTable = HashTable(40)
        temp_nodes: list["Node"] = []
        for node in self.nodes:
            address: str = node.node_address
            if address in package_addresses or address == "HUB":
                node.calculate_priority(truck.packages)
                package_nodes.insert(address, node)
                temp_nodes.append(node)

        filtered_edges: HashTable = HashTable(40)
        for edge in self.edges:
            if edge.eligible(temp_nodes):
                origin: str = edge.origin.node_address
                destination: str = edge.destination.node_address
                edge.calculate_priority()
                filtered_edges.insert((origin, destination), edge)

        return Graph(package_nodes, filtered_edges)

    def get_truck_path(self, truck: "Truck"):
        truck.delivery_graph = self.filter_truck_graph(truck)
        truck.determine_path()

    def deliver_packages(self):
        for driver in self.drivers:
            driver.select_truck(self.trucks)

        trucks_returned: int = 0
        while trucks_returned < NUMBER_OF_TRUCKS:
            for truck in self.trucks:
                if truck.driver is None:
                    continue

                truck.go_to_next_node(truck.delivery_path.pop(0))
                if len(truck.delivery_path) > 0:
                    truck.deliver_package()
                else:
                    trucks_returned += 1
                    truck.returned = True
                    truck.driver.select_truck(self.trucks)
                    truck.driver = None

    def cli(self):
        user_hour: int = 0
        user_minute: int = 0
        user_second: int = 0
        while True:
            try:
                user_hour = int(input("Enter the hour you would like to check: "))
                if user_hour < 8 or user_hour > 24:
                    raise ValueError()
                break
            except ValueError:
                print("Please input an integer between 8 and 24")

        while True:
            try:
                user_minute = int(input("Enter the minute you would like to check: "))
                if user_minute < 0 or user_minute > 60:
                    raise ValueError()
                break
            except ValueError:
                print("Please input an integer between 0 and 60")

        while True:
            try:
                user_second = int(input("Enter the second you would like to check: "))
                if user_second < 0 or user_second > 60:
                    raise ValueError()
                break
            except ValueError:
                print("Please input an integer between 0 and 60")

        user_time: datetime = datetime.now().replace(
            hour=user_hour,
            minute=user_minute,
            second=user_second,
            microsecond=0
        )

        print(f"\nTime entered: {user_time}")
        for package_id in range(self.packages.table_items):
            package_status: str = "Not Delivered"
            package: "Package" = self.packages.lookup(package_id + 1)
            if package.delivered_time < user_time:
                package_status = "Delivered"
            print(package.package_id, package_status)

        distance: int = 0
        for truck in self.trucks:
            distance += truck.distance_traveled

        print(f"\n{distance} Miles traveled")


def main() -> None:
    Application().start()


if __name__ == "__main__":
    main()
