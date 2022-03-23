from utils import generate_next_prime


class HashTable:
    def __init__(self, initial_capacity = 10):
        self.initial_capacity = generate_next_prime(initial_capacity)
        self.table = []
        self.table_items = 0

        for _ in range(initial_capacity):
            self.table.append([])

    def get(self, key):
        index = self._hash_key(key, len(self.table))
        if self.table[index] is None:
            return None

        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]

    def insert(self, key, value):
        load_factor = self.table_items / len(self.table)
        if load_factor > .8:
            self._resize()

        index = self._hash_key(key, len(self.table))
        for pair in self.table[index]:
            if pair[0] is not key:
                self.table_items += 1

        self._add_pair(key, value, self.table)

    def remove(self, key):
        index = self._hash_key(key, len(self.table))
        if self.table[index] is None:
            return None

        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                return self.table[index].pop(i)

    def _hash_key(self, key, table_len):
        return hash(key) % table_len

    def _resize(self):
        new_table = []
        for _ in range(generate_next_prime(len(self.table) * 2)):
            new_table.append([])

        for item in new_table:
            if item is not None:
                for key, value in item:
                    self._add_pair(key, value, new_table)

        self.table = new_table

    def _add_pair(self, key, value, table):
        index = self._hash_key(key, len(table))
        if table[index] is None:
            table.append([key, value])
        else:
            table[index] = [[key, value]]
