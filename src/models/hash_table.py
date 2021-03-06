from typing import Any
from utilities.primes import generate_next_prime


class HashTable:
    def __init__(self, initial_capacity: int = 10) -> None:
        """
        Constructor to initialize a HashTable.\n
        Space-time complexity: O(N)
        """

        # Converts the initial capacity to a prime number to improve the hashing efficiency
        self.initial_capacity: int = generate_next_prime(initial_capacity)
        self.table: list[list[Any]] = []
        self.table_items: int = 0

        # Initializes the table with empty lists up to the initial capacity
        for _ in range(initial_capacity):
            self.table.append([])

    def __repr__(self) -> str:
        """
        Repr method to represent a hashtable.\n
        Space-time complexity: O(1)
        """

        return f"Capacity: {len(self.table)}, Total Items: {self.table_items}, Pairs: {self.table}"

    def lookup(self, key: Any) -> Any:
        """
        Lookup function to search for a specific value associated with a provided key. If the keys hash is not present,
        return None, otherwise, loop through each key at the matching hash index until a match is found, then return the
        associated value.\n
        Space complexity: O(1)\n
        Time complexity: O(N)
        """

        index: int = hash_key(key, len(self.table))
        if self.table[index] is None:
            return None

        # If a match is found, loop through each key value pair present at the index until a match is found, usually
        # There will only be one key value pair at the provided index
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]

    def insert(self, key: Any, value: Any) -> None:
        """
        Insert function to insert a key value pair into the hash table. In the case where the key already exists in the
        table, the value will be replaced with the new value (doubles as a modify function).\n
        Space complexity: O(1)\n
        Time complexity: O(N)
        """

        load_factor: float = self.table_items / len(self.table)
        if load_factor >= .8:
            self._resize()

        index: int = hash_key(key, len(self.table))
        # If a key already exists in the table matching the provided key, replace that keys value and do not increment
        # the table items
        increment: bool = True
        for pair in self.table[index]:
            if pair[0] is key:
                increment = False
        if increment:
            self.table_items += 1

        add_pair(key, value, self.table, index)

    def remove(self, key: Any) -> Any:
        """
        Remove function to pop a matching key value pair from the table and if a match exists, the value is returned.\n
        Space complexity: O(1)\n
        Time complexity: O(N)
        """

        index = hash_key(key, len(self.table))
        if self.table[index] is None:
            return None

        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                self.table_items -= 1
                return self.table[index].pop(i)[1]

    def _resize(self) -> None:
        """
        A resize function that increases the size of the hash table whenever a load limit is hit. This is done to ensure
        that matching hashes are much less frequent, leading towards better lookup efficiency down the road. This is
        done by creating a new table that is about twice the size of the previous table and re-hashing each key value
        pair within the table\n
        Space complexity: O(N)\n
        Time complexity: O(N + MP)
        """

        new_table: list[list[Any]] = []
        for _ in range(generate_next_prime(len(self.table) * 2)):
            new_table.append([])

        for item in self.table:
            if item is not None:
                for key, value in item:
                    add_pair(key, value, new_table, hash_key(key, len(self.table)))
        self.table = new_table


def hash_key(key: Any, table_len: int) -> int:
    """
    Given a key value calculate the index of the table that the value will be stored in.\n
    Space-time complexity: O(1)
    """

    return hash(key) % table_len


def add_pair(key: Any, value: Any, table: list[list[Any]], index: int) -> None:
    """
    Function to append a key value pair to a given table at the given index.\n
    Space-time complexity: O(1)
    """

    if table[index] is None:
        table[index] = [key, value]
    else:
        table[index].append([key, value])
