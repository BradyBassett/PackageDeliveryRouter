"""
First
Last
ID
"""

from utilities.hash_table import HashTable

table = HashTable()

print(len(table.table))
table.insert(1, "peee")
table.insert("hi", "pooo")
table.insert("hi", "sdfsdfg")
table.insert("fg", "sdfg")
print(len(table.table))
table.insert("sdfgsdg", "sdfsdfr")


print(table.get("hi"))
print(table.remove("hi"))
print(table.get("hi"))

