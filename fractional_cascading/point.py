from typing import Tuple


class Point:
    def __init__(self, name: str, loc: Tuple[float], **kwargs):
        assert len(loc) == 2
        self.name = name
        self.__loc = *loc, self.name
        self.attr = kwargs

    def loc(self) -> Tuple[float, str]:
        return self.__loc

    def loc_rev(self) -> Tuple[float]:
        return self.__loc[1], self.__loc[0]

    def is_included(self, com_R) -> bool:
        lon, lat, _ = self.__loc
        return (
            com_R.x_min <= (lon, lat) <= com_R.x_max
            and com_R.y_min <= (lat, lon) <= com_R.y_max
        )

    def __hash__(self):
        return hash((self.name, self.__loc))

    def __repr__(self):
        return f"Point{self.name, self.__loc[:2]})"
