from typing import List, Tuple
from .point import Point


class FCPoint:
    def __init__(self, point: Point):
        self.point = point
        self.bleft = None  # left_begin_pointer
        self.bright = None  # right_begin_pointer
        self.eleft = None  # left_end_pointer
        self.eright = None  # left_end_pointer

    def loc(self) -> Tuple[float, str]:
        return self.point.loc()

    def loc_rev(self) -> Tuple[float]:
        return self.point.loc_rev()

    def is_included(self, com_R) -> bool:
        return self.point.is_included(com_R)

    def find_minmax_ix(self, array: List[Point]) -> int:
        """
        Returns:
            int: minmax index of array for (y, x)
        """
        lo, hi = 0, len(array)
        if self.loc_rev() > array[hi - 1].loc_rev():
            return None
        while lo < hi:
            mid = (lo + hi) // 2
            if array[mid].loc_rev() < self.loc_rev():
                lo = mid + 1
            else:
                hi = mid
        return lo

    def find_maxmin_ix(self, array: List[Point]) -> int:
        """
        Returns:
            int: minmax index of array for (y, x)
        """
        lo, hi = 0, len(array)
        if self.loc_rev() < array[lo].loc_rev():
            return None
        while lo < hi:
            mid = (lo + hi) // 2
            if self.loc_rev() < array[mid].loc_rev():
                hi = mid
            else:
                lo = mid + 1
        return lo - 1
