from typing import Tuple
from .point import Point


class FCNode:
    def __init__(self, point: Point):
        self.point = point
        self.left = None
        self.right = None
        self.array = None

    def loc(self) -> Tuple[float, str]:
        return self.point.loc()

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None
