# 参考書籍: De Berg, Mark, et al. "コンピュータ・ジオメトリ 計算幾何学: アルゴリズムと応用." (2000) 第5章

from typing import List, Tuple, Generator
from .rectangle import Rectangle
from .point import Point
from .fc_point import FCPoint
from .fc_node import FCNode


class Tree:
    def __init__(self, points: List[Point] = None, pickle_file: str = None):
        self.root = None
        if pickle_file is not None:
            import pickle

            with open(pickle_file, "rb") as pf:
                self.root = pickle.load(pf)
        if points is not None:
            self.build_fc_tree(points)

    def query(self, R: Rectangle) -> Generator[FCPoint, None, None]:
        """
        Yields:
            Point: points are include in Rectangle R
        """
        com_R = Rectangle(
            x_min=(R.x_min, -float("inf")),
            x_max=(R.x_max, float("inf")),
            y_min=(R.y_min, -float("inf")),
            y_max=(R.y_max, float("inf")),
        )
        yield from (fc_point.point for fc_point in self.fc_range_query(com_R))

    def build_fc_tree(self, points: List[Point]):
        """build fractional cascading tree from points"""
        assert len(points) > 0, "no points in input data"
        assert len(points) == len(set(points)), "(name, location) data must be unique."
        points = [FCPoint(point) for point in points]

        points.sort(key=lambda point: point.loc())  # sorted by x
        sbx = [FCPoint(fc_point.point) for fc_point in points]
        points.sort(key=lambda point: point.loc_rev())  # sorted by y
        sby = [FCPoint(fc_point.point) for fc_point in points]

        def link_array(
            array: List[FCPoint], array_l: List[FCPoint], array_r: List[FCPoint]
        ) -> List[FCPoint]:
            """create minmax and maxmin link from array to array_l and array_r"""
            for fc_point in array:
                fc_point.bleft = fc_point.find_minmax_ix(array_l)
                fc_point.bright = fc_point.find_minmax_ix(array_r)
                fc_point.eleft = fc_point.find_maxmin_ix(array_l)
                fc_point.eright = fc_point.find_maxmin_ix(array_r)
            return array

        def create_node(sbx: List[FCPoint], sby: List[FCPoint]) -> FCNode:
            if len(sbx) == 1:
                v = FCNode(sbx[0])
                v.array = sby
            else:
                n = len(sbx)
                pivot = sbx[n // 2 - 1]
                sbx_l = sbx[: n // 2]
                sbx_r = sbx[n // 2 :]
                sby_l = [
                    FCPoint(fc_point.point)
                    for fc_point in sby
                    if fc_point.loc() <= pivot.loc()
                ]
                sby_r = [
                    FCPoint(fc_point.point)
                    for fc_point in sby
                    if fc_point.loc() > pivot.loc()
                ]
                v = FCNode(pivot)
                v.array = link_array(sby, sby_l, sby_r)
                v.left = create_node(sbx_l, sby_l)
                v.right = create_node(sbx_r, sby_r)
            return v

        self.root = create_node(sbx, sby)
        return self

    def dump_pickle(self, pickle_file: str):
        import pickle

        with open(pickle_file, "wb") as pf:
            pickle.dump(self.root, file=pf, protocol=-1)

    def find_split_node(self, begin: Tuple[float], end: Tuple[float]) -> FCNode:
        """
        Returns:
            FCNode: FCNode v where the search path to begin and the search path to end diverge, or leaf node v where both paths end together
        """
        v = self.root
        while not v.is_leaf() and not begin <= v.loc() < end:
            if v.loc() >= end:
                v = v.left
            else:
                v = v.right
        return v

    def fc_range_query(self, com_R: Rectangle) -> Generator[FCPoint, None, None]:
        begin_x, end_x = com_R.x_min, com_R.x_max
        begin_y, end_y = com_R.y_min, com_R.y_max
        virtual_begin_point = FCPoint(Point(name="vbe", loc=(begin_y[1], begin_y[0])))
        virtual_end_point = FCPoint(Point(name="vee", loc=(end_y[1], end_y[0])))

        v_split = self.find_split_node(begin_x, end_x)
        minmax_ix = virtual_begin_point.find_minmax_ix(v_split.array)
        maxmin_ix = virtual_end_point.find_maxmin_ix(v_split.array)
        if minmax_ix is None or maxmin_ix is None:
            return None
        minmax_key = v_split.array[minmax_ix]
        maxmin_key = v_split.array[maxmin_ix]

        if v_split.is_leaf():
            if v_split.array[0].is_included(com_R):
                yield v_split.array[0]
        else:

            def frac_casc(array, begin_pointer, end_pointer):
                if begin_pointer is not None and end_pointer is not None:
                    yield from (
                        array[ix] for ix in range(begin_pointer, end_pointer + 1)
                    )

            v = v_split.left
            lb_p = minmax_key.bleft  # left begin pointer
            le_p = maxmin_key.eleft  # left end pointer
            while not lb_p is None and not le_p is None and not v.is_leaf():
                if v.loc() >= begin_x:
                    begin_p = v.array[lb_p].bright
                    end_p = v.array[le_p].eright
                    yield from frac_casc(v.right.array, begin_p, end_p)
                    lb_p = v.array[lb_p].bleft
                    le_p = v.array[le_p].eleft
                    v = v.left
                else:
                    lb_p = v.array[lb_p].bright
                    le_p = v.array[le_p].eright
                    v = v.right
            if not lb_p is None and not le_p is None and v.array[0].is_included(com_R):
                yield v.array[0]

            v = v_split.right
            rb_p = minmax_key.bright  # right begin pointer
            re_p = maxmin_key.eright  # right end pointer
            while not rb_p is None and not re_p is None and not v.is_leaf():
                if v.loc() <= end_x:
                    begin_p = v.array[rb_p].bleft
                    end_p = v.array[re_p].eleft
                    yield from frac_casc(v.left.array, begin_p, end_p)
                    rb_p = v.array[rb_p].bright
                    re_p = v.array[re_p].eright
                    v = v.right
                else:
                    rb_p = v.array[rb_p].bleft
                    re_p = v.array[re_p].eleft
                    v = v.left
            if not rb_p is None and not re_p is None and v.array[0].is_included(com_R):
                yield v.array[0]


if __name__ == "__main__":

    points = list()
    points.append(Point(name="A", loc=(1, 5)))  # loc = (x, y)
    points.append(Point(name="B", loc=(2, 2)))
    points.append(Point(name="C", loc=(4, 8)))
    points.append(Point(name="D", loc=(5, 7)))
    points.append(Point(name="E", loc=(5, 5)))
    points.append(Point(name="F", loc=(8, 6)))
    points.append(Point(name="E", loc=(7, 1)))

    # create Fract Fractional Cascading Tree instance
    tree = Tree(points)
    # save tree as pickle file
    # tree.dump_pickle(pickle_file="sample.pickle")
    # load tree from pickle file
    # tree = Tree(pickle_file="sample.pickle")

    # rectangel as query
    R = Rectangle(x_min=1.5, x_max=5.5, y_min=1.5, y_max=5.5)

    # search points in query
    for point in tree.query(R):
        print(point)
