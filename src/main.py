"""
Brady
Bassett
#002616010
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
FLIGHT_ARRIVED: datetime = datetime.now().replace(hour=9, minute=5, second=0, microsecond=0)
PACKAGE_ADDRESS_CORRECTED: datetime = datetime.now().replace(hour=10, minute=20, second=0, microsecond=0)
CORRECT_PACKAGE_ADDRESS: tuple[str, int] = ("410 South State St", 84111)


class Application:
    def __init__(self) -> None:
        """
        Constructor for the application class to initialize an application object.\n
        Space-time complexity: O(T + D)
        """
        self.packages: HashTable = HashTable()
        self.graph: Graph = Graph()
        self.trucks: list[Truck] = [Truck(i + 1) for i in range(NUMBER_OF_TRUCKS)]
        self.drivers: list[Driver] = [Driver(i + 1) for i in range(NUMBER_OF_DRIVERS)]

    def start(self) -> None:
        """
        This function will begin the delivery simulation.\n
        Space-time complexity: O(N)
        """
        self.load_packages()
        self.load_trucks()
        self.load_nodes()
        self.load_edges()
        self.load_initial_drivers()
        self.deliver_packages()
        self.cli()

    def load_packages(self) -> None:
        """
        This function iterates each row of the packages.csv file and initializes a package object based on the data.\n
        Space-time complexity: O(N)
        """
        with open("data/packages.csv") as file:
            file_data: reader = reader(file)
            for row in file_data:
                package: Package = Package(int(row[0]), row[1], row[2], row[3],
                                           int(row[4]), row[5], int(row[6]), row[7])
                self.packages.insert(package.package_id, package)

    def load_trucks(self) -> None:
        """
        This function takes every package found in the packages.csv file and determines which truck the package should
        be loaded onto.\n
        Space complexity: O(P)\n
        Time complexity: O(NM + P)
        """
        packages: list["Package"] = []

        for package_id in range(self.packages.table_items):
            package: "Package" = self.packages.lookup(package_id + 1)
            # If the package has no special notes
            if package.special_notes == "":
                # If the package is related to packages with "Must be delivered with" in their special notes and loads
                # them onto truck 1
                if package.delivery_deadline or package.package_id in [13, 15, 19,]:
                    self.trucks[0].load_package(package)
                # Otherwise, add them to a list that will be distributed to the spaces remaining on the trucks
                else:
                    packages.append(package)
            # If the package contains special notes
            else:
                # If the package has "Must be delivered with" in the special notes, load it onto truck 1 with the
                # related packages
                if "Must be delivered with" in package.special_notes:
                    self.trucks[0].load_package(package)
                # Otherwise, load all remaining packages onto truck 2
                else:
                    self.trucks[1].load_package(package)

        truck_index: int = 0
        for package in packages:
            if len(self.trucks[truck_index].packages) >= self.trucks[truck_index].capacity:
                truck_index += 1
            self.trucks[truck_index].load_package(package)

    def load_nodes(self) -> None:
        """
        This function takes the data from the addresses.csv file to generate all the nodes in the delivery graph.\n
        Space-time complexity: O(N)
        """
        with open("data/addresses.csv") as file:
            file_data: reader = reader(file)
            for row in file_data:
                node: "Node" = Node(int(row[0]), row[1], row[2], row[3])
                self.graph.add_node(node)

    def load_edges(self) -> None:
        """
        This function takes the data from the distances.csv file to generate all the edges and their distances in the
        delivery graph.\n
        Space complexity: O(N)\n
        Time complexity: O(N^2)
        """
        with open("data/distances.csv") as file:
            file_data: reader = reader(file)
            for i, row in enumerate(file_data):
                for j in range(i):
                    if i is not j:
                        edge: "Edge" = Edge(self.graph.nodes_list[j], self.graph.nodes_list[i], float(row[j]))
                        self.graph.add_edge(edge)

    def load_initial_drivers(self) -> None:
        """
        This function loops through both drivers and has them select the first two trucks to load themselves into. The
        driver who loads into the second truck will be delayed until the flight arrival time. Then for each package on
        the selected truck, the package's departure time is set equal to the driver's current time.\n
        Space complexity: O(1)\n
        Time complexity: O(DP)
        """
        for driver in self.drivers:
            driver.select_truck(self.trucks)
            if driver.current_truck.truck_id == 2:
                driver.current_time = FLIGHT_ARRIVED
            driver.current_truck.filter_truck_graph(self.graph)
            driver.current_truck.determine_path()
            for package in driver.current_truck.packages:
                package.departure_time = driver.current_time

    def change_truck(self, truck: "Truck") -> None:
        """
        This function will return a truck to the hub and have its driver select a new truck to operate. It will also
        set each package's departure time, on the new truck, to the drivers current time.\n
        Space complexity: O(1)\n
        Time complexity: O(N)
        """
        truck.driver.select_truck(self.trucks)
        truck.returned = True
        truck.driver.current_truck.filter_truck_graph(self.graph)
        truck.driver.current_truck.determine_path()
        for package in truck.driver.current_truck.packages:
            package.departure_time = truck.driver.current_time
        truck.driver = None

    def deliver_packages(self) -> None:
        """
        This function represents the primary delivery loop to traverse each truck through its delivery path, delivering
        every package it has to their appropriate delivery locations. Also, whenever the driver of the second truck has
        their current time pass 10:20, the package with the incorrect delivery address will be corrected, and the
        delivery path will be adjusted to match the new address.\n
        Space complexity: O(1)\n
        Time complexity: O(PTN)
        """
        packages_delivered: int = 0
        while packages_delivered < self.packages.table_items:
            for truck in self.trucks:
                if not truck.driver:
                    continue

                # This simulates the WGUPS receiving the correct package address at 10:20 and adjusts the trucks' path
                # according to the new package address
                if truck.truck_id == 2 and truck.driver.current_time >= PACKAGE_ADDRESS_CORRECTED:
                    for package in truck.packages:
                        if package.special_notes == "Wrong address listed":
                            package.address = CORRECT_PACKAGE_ADDRESS[0]
                            package.zipcode = CORRECT_PACKAGE_ADDRESS[1]
                            break
                    truck.filter_truck_graph(self.graph)
                    truck.determine_path()

                truck.go_to_next_node()

                if len(truck.delivery_path) > 0:
                    packages_delivered += truck.deliver_package()
                else:
                    self.change_truck(truck)

    def cli(self):
        """
        This method represents the command line interface that the user will interact with to see the package status
        at whatever time the user would like. At the end of the application every package and the package status will
        be displayed along with the total distance traveled by each truck.\n
        Space complexity: O(1)\n
        Time complexity: O(H + M + S + P + T)
        """
        while True:
            try:
                user_hour: int = int(input("Enter the hour you would like to check: "))
                if user_hour < 8 or user_hour > 23:
                    raise ValueError()
                break
            except ValueError:
                print("Please input an integer between 8 and 23")

        while True:
            try:
                user_minute: int = int(input("Enter the minute you would like to check: "))
                if user_minute < 0 or user_minute > 59:
                    raise ValueError()
                break
            except ValueError:
                print("Please input an integer between 0 and 59")

        while True:
            try:
                user_second: int = int(input("Enter the second you would like to check: "))
                if user_second < 0 or user_second > 59:
                    raise ValueError()
                break
            except ValueError:
                print("Please input an integer between 0 and 59")

        user_time: datetime = datetime.now().replace(
            hour=user_hour,
            minute=user_minute,
            second=user_second,
            microsecond=0
        )

        print(f"\nTime entered: {user_time}")
        for package_id in range(self.packages.table_items):
            package: "Package" = self.packages.lookup(package_id + 1)

            if package.delivered_time and package.delivered_time < user_time:
                package.delivery_status = "Delivered"
            elif package.departure_time and package.departure_time < user_time:
                package.delivery_status = "En route"
            print(package)

        distance: int = 0
        for truck in self.trucks:
            distance += truck.distance_traveled

        print(f"\n{distance} Miles traveled")


def main() -> None:
    """
    Entry point of the application\n
    Space-time complexity: O(1)
    """
    Application().start()


if __name__ == "__main__":
    main()
