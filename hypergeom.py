import drawsvg as dw
import random as rd
from abc import ABC, abstractmethod


class Element:
    """
    An element in a K-radius Hyperbolic Plane
    """
    @abstractmethod
    def as_svg(self):
        pass


class Point:
    """
    A point in a hyperbolic plane which is defined by two coordinates. These coordinates must
    fall into the plane which is defined by a radius-K circle (not including edges).

    Parameters:
        x, x coordinate (real number)
        y, y coordinate (real number)
    """
    def __init__(self, x, y):
        if self._valid_coords(x, y):
            self._x = x
            self._y = y
        else:
            raise ValueError(f'Point must be within 1-radius circle (x^2 + y^2 < 1)')

    def __str__(self):
        return f'({self._x}, {self._y})'

    def _valid_coords(self, x, y):
        # assumes point is in hyperbolic plane where K = 1
        # all points must be within radius-1 circle (non-inclusive)
        return x**2 + y**2 < 1

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, new_y):
        self._y = new_y

    @property
    def coords(self):
        return self._x, self._y
    @coords.setter
    def coords(self, new_x, new_y):
        self._x = new_x
        self._y = new_y

    def collinear(self, *points):
        if len(points) < 2:
            return True
        matched_slope = slope(self, points[0])
        for i in range(1, len(points)):
            if abs(matched_slope - slope(points[i-1], points[i])) > 0.0001:
                return False
        return True

    def as_svg(self):
        return dw.Circle(self.x, self.y, .03,
                         stroke='black',
                         stroke_width=0.01,
                         fill='black')


class Line:
    """
    A line in the hypergeometric plane is defined the same as it is in the Euclidian plane:
        Passes through two points
        Can be extended forever (to the line at infinity in our case)

    In Poincare's disk representation, the line is drawn as a circular arc which passes through two
    defined points. The arc must intercept the line at infinity (K-radius Circle which acts as edge
    of the plane) perpendicularly.

    Parameters:
        point1, point in hyperbolic plane
        point2, point in hyperbolic plane
    """
    def __init__(self, point1: Point, point2: Point):
        self._point1 = point1
        self._point2 = point2

    def __str__(self):
        return f'Line from {self._point1} to {self._point2}'

    @property
    def point1(self):
        return self._point1
    @point1.setter
    def point1(self, new_point1: Point):
        self._point1 = new_point1

    @property
    def point2(self):
        return self._point2
    @point2.setter
    def point1(self, new_point2: Point):
        self._point2 = new_point2

    def midpoint(self):
        x1, y1 = self._point1.coords
        x2, y2 = self._point2.coords
        return Point((x2 + x1) / 2, (y2 + y1) / 2)

    def as_svg(self):
        origin = Point(0, 0)
        print(self)
        print(origin.collinear(self.point1, self.point2))
        if origin.collinear(self._point1, self._point2):
            print('wa')
            x1, y1 = self._point1.coords
            mag1 = (x1**2 + y1**2)**0.5
            x2, y2 = self._point2.coords
            mag2 = (x2**2 + y2**2)**0.5
            # normalize line to extend across entire plane
            return dw.Line(x1/mag1, y1/mag1, x2/mag2, y2/mag2,
                           stroke='black',
                           stroke_width=0.01)

        a, b, r = self.corresponding_circle()
        return dw.Circle(a, b, r,
                         stroke='black',
                         stroke_width=0.01,
                         fill='none',
                         clip_path='url(#unit_circle)')

    def corresponding_circle(self):
        # lines are drawn as a circle (defined as a^2 + b^2 = r^2) which must:
        #   pass thorugh point1 and point2
        #   intercept a circle (defined as x^2 + y^2 = K^2) perpendicularly
        #
        # Mathemetically, these constraints look like:
        #   (x1 - a)^2 + (y1 - b)^2 = r^2
        #   (x2 - a)^2 + (y2 - b)^2 = r^2
        #   K^2 + r^2 = a^2 + b^2 (via Pythagoran Theorum)
        #
        # With three equations and three unknowns we can define a, b, and r in terms of
        # x1, y1, x2, y2, and K. To make the algebra simpler, we combine some expressions of
        # constants into their own constants.

        x1, y1 = self._point1.coords
        x2, y2 = self._point2.coords
        R = 1

        c1 = float(x1 - x2)
        c2 = float(y1 - y2)
        c3 = (x1**2 + y1**2 - x2**2 - y2**2) / 2
        
        c4 = (x1**2 + y1**2 + R**2) / 2

        c5 = c1*y1 - c2*x1

        a = (c3*y1 - c2*c4) / c5
        b = (c1*c4 - c3*x1) / c5
        r = (a**2 + b**2 - R**2)**0.5

        return a, b, r


class LineSegment(Line):
    def __init__(self, point1, point2):
        super().__init__(point1, point2)

    def euclidian_length(self):
        x1, y1 = self._point1.coords
        x2, y2 = self._point2.coords
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

    def as_svg(self):
        origin = Point(0, 0)
        x1, y1 = self._point1.coords
        x2, y2 = self._point2.coords
        if origin.collinear(self._point1, self._point2):
            return dw.Line(x1, y1, x2, y2,
                           stroke='black',
                           stroke_width=0.01)

        a, b, r = self.corresponding_circle()

        midx, midy = self.midpoint().coords
        radius = self.euclidian_length() / 2
        clip = dw.ClipPath()
        clip.append(dw.Circle(midx, midy, radius))
        return dw.Circle(a, b, r,
                         stroke='black',
                         stroke_width=0.01,
                         fill='none',
                         clip_path=clip)


class HyperbolicPlane:
    # TODO: complete  docstring
    """
    A hyperbolic plane with a defined K. Contains a set of Elements. Can be visualized as either...
    """
    def __init__(self):
        self._elements = set()

    def add(self, to_add: Element):
        self._elements.add(to_add)

    def remove(self, to_remove: Element):
        self._elements.remove(to_remove)

    def make_svg(self, filename, show_loi=True):
        drawing = dw.Drawing(800, 800, viewBox='-1.1 -1.1 2.2 2.2')
        if show_loi:
            drawing.append(dw.Circle(0, 0, 1,
                                     stroke='black',
                                     stroke_width=.01,
                                     stroke_dasharray='0.05, 0.05',
                                     fill='none'))

        boundary = dw.ClipPath(id='unit_circle')
        boundary.append(dw.Circle(0, 0, 1))
        drawing.append_def(boundary)

        for element in self._elements:
            print(f'Drawing {element}')
            drawing.append(element.as_svg())
        drawing.append(dw.Line(0, 0, 1, 1))
        drawing.save_svg(filename)


# Helper Geometric Functions
def slope(point1: Point, point2: Point) -> float:
    x1, y1 = point1.coords
    x2, y2 = point2.coords

    delta_y = y2 - y1
    delta_x = x2 - x1

    if delta_x == 0:
        return float('inf')
    else:
        return delta_y / delta_x


def main():
    plane = HyperbolicPlane()

    o = Point(0, 0)
    point1 = Point(0.5, -0.5)
    point2 = Point(0.5, 0)
    point3 = Point(-0.5, 0.5)

    line1 = LineSegment(point1, point2)
    line2 = LineSegment(point1, point3)

    plane.add(point1)
    plane.add(point2)
    plane.add(point3)
    plane.add(line1)
    plane.add(line2)

    plane.make_svg('drawings/test.svg')





if __name__ == '__main__':
    main()



