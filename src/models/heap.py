from typing import TYPE_CHECKING, Optional
from math import frexp
from tree import Tree

if TYPE_CHECKING:
    from node import Node


class Heap:
    def __init__(self) -> None:
        self.trees: list["Tree"] = []
        self.min: Optional["Tree"] = None
        self.count: int = 0

    def insert(self, node: "Node") -> None:
        temp_tree: "Tree" = Tree(node)
        self.trees.append(temp_tree)
        if self.min is None or node.weight < self.min.value.weight:
            self.min = temp_tree
        self.count += 1

    def extract_min(self) -> "Node":
        least: "Tree" = self.min

        if least is not None:
            for child in least.child:
                self.trees.append(child)
            self.trees.remove(least)
            if not self.trees:
                self.min = None
            else:
                self.min = self.trees[0]
                self.consolidate()
            self.count -= 1
            return least.value

    def consolidate(self):
        temp: list[Optional["Tree"]] = frexp(self.count)[1] * [None]

        while self.trees:
            x: "Tree" = self.trees[0]
            order: int = x.order
            self.trees.remove(x)
            while temp[order] is not None:
                y: "Tree" = temp[order]
                if x.value.weight > y.value.weight:
                    x, y = y, x
                x.append_tree(y)
                temp[order] = None
                order += 1
            temp[order] = x
        self.min = None
        for tree in temp:
            if tree is not None:
                self.trees.append(tree)
                if self.min is None or tree.value.weight < self.min.value.weight:
                    self.min = tree
