import drawsvg as dw
from abc import ABC, abstractmethod


class Element(ABC):
    """
    An element in a K-radius Hyperbolic Plane

    Parameters:
        K (1 default), #TODO define K
    """
    def __init__(self, K=1):
        self._K = K

    @abstractmethod
    def as_svg(self):
        pass


class Point(Element):
    """
    A point in a hyperbolic plane which is defined by two coordinates. These coordinates must
    fall into the plane which is defined by a radius-K circle (not including edges).

    Parameters:
        x, x coordinate (real number)
        y, y coordinate (real number)
    """
    def __init__(self, x, y):
        if self._valid_coords(x, y, self._K):
            self.x = x
            self.y = y
        else:
            raise ValueError(f'Point must be within K-radius circle (K={self._K})')

    def _valid_coords(self, x, y, K):
        # assumes point is in hyperbolic plane where K = 1
        # all points must be within radius-1 circle (non-inclusive)
        return x**2 + y**2 < K

    def as_svg(self):
        return dw.Circle(self.x, self.y, 1,
                         stroke='black',
                         fill='none')


class Line(Element):
    """
    A line in a hyperbolic plane is, similarly to the Euclidian Plane, is defined by two coordinates.

    Parameters:
        point1, point in hyperbolic plane
        point2, point in hyperbolic plane
    """
    def __init__(self, point1: Point, point2: Point):
        self.__point1 = point1
        self.__point2 = point2

    @property
    def point1(self):
        return self.__point1

    @point1.setter
    def point1(self, new_point1: Point):
        self.__point1 = new_point1

    @property
    def point2(self):
        return self.__point2

    @point2.setter
    def point1(self, new_point2: Point):
        self.__point2 = new_point2

    def as_svg(self):



class HyperbolicPlane(self):
    # TODO: complete  docstring
    """
    A hyperbolic plane with a defined K. Contains a set of Elements. Can be visualized as either...

    Parameters:
        K (default 1), somethin
    """
    def __init__(self, K=1):
        self.__K = K
        self.__elements = set()

    def add(to_add: Element):
        self.__elements.add(to_add)

    def remove(to_remove: Element):
        self.__elements.remove(to_remove)



    
