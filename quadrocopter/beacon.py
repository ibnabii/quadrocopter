from math import sqrt


class Beacon:
    def __init__(self, position_x: int, position_y: int, radius: int):
        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius

    def is_point_in_range(self, x: int, y: int, extend: int = 0) -> bool:
        """
        Checks if position is within range of the beacon assuming Euclidean distance between points
        :param x: coordinate X of the tested position
        :param y: coordinate Y of the tested position
        :param extend: (optional) value by which the radius of the beacon range is extended for test
        :return: True if distance between beacon and tested position is less or equal (beacon's radius + extend).
            False otherwise
        """

        distance = sqrt((self.position_x - x) ** 2 + (self.position_y - y) ** 2)
        return distance <= self.radius + extend

    def is_beacon_in_range(self, other: 'Beacon') -> bool:
        """
        Checks if other Beacon's range overlap with self
        :param other: Beacon to test
        :return: True if distance between beacons is less or equal sum of their radiuses
        """
        return self.is_point_in_range(other.position_x, other.position_y, other.radius)
