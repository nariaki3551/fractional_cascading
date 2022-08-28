# fractional_cascading

Fractional cascading python api for 2-dimension points.
This is the fast search algorithm to find the 2-dimensional points (x, y) in a rectangle.

## Install

```
git clone https://github.com/nariaki3551/fractional_cascading.git
cd fractional_cascading
```
and

```
pip install .
# or, python setup.py install
```


## Example

```python
# create points
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
```
