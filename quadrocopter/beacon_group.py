from quadrocopter import Beacon


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
