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


class BeaconGroup:
    def __init__(self, first_beacon: Beacon = None):
        if first_beacon:
            self.beacons = [Beacon]
        else:
            self.beacons = []

    def add(self, beacon: Beacon) -> None:
        """
        Adds beacon to the group
        :param beacon: beacon to add
        :return: None
        """
        self.beacons.append(beacon)

    def is_point_in_range(self, x: int, y: int, extend: int = 0) -> bool:
        """
        Checks if position is within range of any beacon in the group assuming Euclidean distance between points
        :param x: coordinate X of the tested position
        :param y: coordinate Y of the tested position
        :param extend: (optional) value by which the radius of the beacon range is extended for test
        :return: True if distance between any beacon in group and tested position is
            less or equal (beacon's radius + extend). False otherwise.
        """
        for beacon in self.beacons:
            if beacon.is_point_in_range(x, y, extend):
                return True
        return False

    def is_beacon_in_range(self, other: Beacon) -> bool:
        """
        Checks if other Beacon's range overlap with any beacon in the group
        :param other: Beacon to test
        :return: True if other Beacon's range overlap with any beacon in the group, False otherwise
        """
        return self.is_point_in_range(other.position_x, other.position_y, other.radius)


class World:
    def __init__(self):
        self.groups: list[BeaconGroup] = []

    def get_overlapping_groups(self, beacon: Beacon) -> tuple[BeaconGroup]:
        """
        Finds beacon groups that the beacon overlaps range with.
        :param beacon: Beacon to test
        :return: Tuple of beacon groups. Tuple containing an empty beacon group if beacon does not overlap
        with any of the existing groups.
        """
        groups = []
        for group in self.groups:
            if group.is_beacon_in_range(beacon):
                groups.append(group)
        if len(groups):
            return tuple(groups)
        else:
            self.groups.append(BeaconGroup())
            return (self.groups[-1],)

    def add(self, beacon: Beacon):
        """
        Adds a beacon to the World. Beacon is added to the group it overlaps with.
        New group is created if beacon does not overlap with any group.
        If new beacon overlaps with many groups, they are merged into one
        :param beacon:
        :return:
        """
        groups = self.get_overlapping_groups(beacon)

        # add beacon to first group
        groups[0].add(beacon)

        # merge other groups
        for group in groups[1:]:
            groups[0].beacons += group.beacons
            self.groups.remove(group)

    def is_there_path(self, point1: tuple[int, int], point2: tuple[int, int]):
        """
        Checks if there is a path within coverage of beacons between point1 and point2
        :param point1: tuple (x, y) denoting position of first point
        :param point2: tuple (x, y) denoting position of second point
        :return: True if quadrocopter can travel from point1 to point2, False otherwise
        """
        for group in self.groups:
            if group.is_point_in_range(*point1):
                if group.is_point_in_range(*point2):
                    return True
                else:
                    return False
        return False


