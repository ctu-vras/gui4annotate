#!/usr/bin/env python3

import numbers


class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if isinstance(other, Vec2D):
            return Vec2D(self.x * other.x, self.y * other.y)
        if isinstance(other, numbers.Number):
            return Vec2D(self.x * other, self.y * other)
        raise TypeError('Cannot multiply vector with something else')

    def __add__(self, other):
        if isinstance(other, Vec2D):
            return Vec2D(self.x + other.x, self.y + other.y)
        if isinstance(other, numbers.Number):
            return Vec2D(self.x + other, self.y + other)
        raise TypeError('Cannot add vector with something else')

    def __neg__(self):
        return Vec2D(-self.x, -self.y)

    def __sub__(self, other):
        if isinstance(other, Vec2D):
            return Vec2D(self.x - other.x, self.y - other.y)
        if isinstance(other, numbers.Number):
            return Vec2D(self.x * other, self.y * other)
        raise TypeError('Cannot substract vector with something else')

    def __truediv__(self, other):
        if isinstance(other, Vec2D):
            return Vec2D(self.x / other.x, self.y / other.y)
        if isinstance(other, numbers.Number):
            return Vec2D(self.x / other, self.y / other)
        raise TypeError('Cannot divide vector with something else')

    def __iadd__(self, other):
        return self.__add__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __isub__(self, other):
        return self.__sub__(other)

    def __itruediv__(self, other):
        return self.__truediv__(other)

    def __gt__(self, other):
        if isinstance(other, Vec2D):
            return self.x > other.x and self.y > other.y
        if isinstance(other, numbers.Number):
            return self.x > other and self.y > other
        raise TypeError('Cannot compare vector with something else')

    def __lt__(self, other):
        if isinstance(other, Vec2D):
            return self.x < other.x and self.y < other.y
        if isinstance(other, numbers.Number):
            return self.x < other and self.y < other
        raise TypeError('Cannot compare vector with something else')

    def __ge__(self, other):
        if isinstance(other, Vec2D):
            return self.x >= other.x and self.y >= other.y
        if isinstance(other, numbers.Number):
            return self.x >= other and self.y >= other
        raise TypeError('Cannot compare vector with something else')

    def __le__(self, other):
        if isinstance(other, Vec2D):
            return self.x <= other.x and self.y <= other.y
        if isinstance(other, numbers.Number):
            return self.x <= other and self.y <= other
        raise TypeError('Cannot compare vector with something else')

    def __eq__(self, other):
        if isinstance(other, Vec2D):
            return self.x == other.x and self.y == other.y
        if isinstance(other, numbers.Number):
            return self.x == other and self.y == other
        raise TypeError('Cannot compare vector with something else')

    def __ne__(self, other):
        return self.__eq__(other)

    def __hash__(self):
        return hash(self.x) + hash(self.y)

    def __round__(self, n=None):
        round(self.x, n)
        round(self.y, n)
        return self

    @staticmethod
    def allmin(*args):
        x = [vec.x for vec in args]
        y = [vec.y for vec in args]
        return Vec2D(min(x), min(y))

    @staticmethod
    def allmax(*args):
        x = [vec.x for vec in args]
        y = [vec.y for vec in args]
        return Vec2D(max(x), max(y))


