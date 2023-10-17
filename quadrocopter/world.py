from quadrocopter import Beacon, BeaconGroup


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

    def is_there_path(self, point1: tuple[int], point2: tuple[int]):
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
