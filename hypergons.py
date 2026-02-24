import numpy as np
from hypergeom import *

class RegularPolygon(Element):
    def __init__(self, num_sides: int, internal_angle: float, in_degrees=True, center=Point(0, 0)):
        if in_degrees:
            internal_angle *= np.pi / 180
                
        if self._valid_inputs(num_sides, internal_angle):
            self._n = num_sides
            self._angle = internal_angle
            self._center = center

            self._points = self.find_points()
            self._lines = self.find_lines()
        else:
            raise ValueError(f'Internal angles for an {num_sides}-gon must be less than {(num_sides-2)*(180 / num_sides)} degrees or {(num_sides-2)*(np.pi / num_sides):.2f} radians')

    def _valid_inputs(self, n, angle):
        return angle < (n - 2) * (np.pi / n)

    def as_svg(self, show_center=False):
        n_gon = dw.Group(id=f'{self._n}-gon', fill='none', stroke='black')
        if show_center:
            n_gon.append(self._center)
        for line in self._lines:
            n_gon.append(line.as_svg())

        return n_gon

    def area(self):
        return np.pi - self.angle*n

    def hyperbolic_circumradius(self):
        cosh_R = np.cos(np.pi / self._n) / np.sin(self._angle / 2)
        return np.arccosh(cosh_R)

    def euclidian_circumradius(self):
        # assuming centered at origin
        R = self.hyperbolic_circumradius()
        return np.tanh(R)

    def find_points(self):
        # 
        r = self.euclidian_circumradius()
        points = []
        for k in range(self._n):
            theta = ((2 * np.pi) / self._n) * k
            points.append(Point(r*np.cos(theta), r*np.sin(theta)))

        points = [mobius_transform(point, self._center) for point in points]

        return points

    def find_lines(self):
        lines = set()
        for i in range(self._n):
            lines.add(LineSegment(self._points[i], self._points[i-1]))
        return lines


def mobius_transform(point: Point, destination: Point):
    temp = (point + destination) / (1 + destination.conjugate() * point)
    return temp.conjugate()


def main():
    plane = HyperbolicPlane()
    shape = RegularPolygon(20, 130)

    plane.add(shape)

    plane.make_svg('drawings/shape.svg')

if __name__ == '__main__':
    main()





