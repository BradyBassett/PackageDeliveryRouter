from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from node import Node


class Tree:
    def __init__(self, value: "Node", priority: int) -> None:
        self.value: "Node" = value
        self.priority: int = priority
        self.child: list["Tree"] = []
        self.order: int = 0

    def append_tree(self, tree: "Tree") -> None:
        self.child.append(tree)
        self.order += 1
