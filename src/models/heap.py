from typing import TYPE_CHECKING, Optional
from math import frexp

if TYPE_CHECKING:
    from node import Node
    from tree import Tree


class Heap:
    def __init__(self) -> None:
        self.trees: list["Tree"] = []
        self.min: Optional["Tree"] = None
        self.count: int = 0

    def insert(self, tree: "Tree") -> None:
        self.trees.append(tree)
        if self.min is None or tree.priority < self.min.priority:
            self.min = tree
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

    def consolidate(self) -> None:
        temp: list[Optional["Tree"]] = frexp(self.count)[1] * [None]

        while self.trees:
            x: "Tree" = self.trees[0]
            order: int = x.order
            self.trees.remove(x)
            while temp[order] is not None:
                y: "Tree" = temp[order]
                if x.priority > y.priority:
                    x, y = y, x
                x.append_tree(y)
                temp[order] = None
                order += 1
            temp[order] = x
        self.min = None
        for tree in temp:
            if tree is not None:
                self.trees.append(tree)
                if self.min is None or tree.priority < self.min.priority:
                    self.min = tree
