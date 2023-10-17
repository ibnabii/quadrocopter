import unittest
from quadrocopter import Beacon, BeaconGroup, World


class TestBeacon(unittest.TestCase):
    def test_basic_init(self):
        beacon = Beacon(1, 2, 3)
        self.assertEqual(beacon.position_x, 1)
        self.assertEqual(beacon.position_y, 2)
        self.assertEqual(beacon.radius, 3)

    def test_point_in_range(self):
        beacon = Beacon(3, 3, 2)
        self.assertEqual(True, beacon.is_point_in_range(3, 3))
        self.assertEqual(True, beacon.is_point_in_range(1, 3))
        self.assertEqual(True, beacon.is_point_in_range(3, 1))
        self.assertEqual(True, beacon.is_point_in_range(5, 3))
        self.assertEqual(True, beacon.is_point_in_range(3, 5))
        self.assertEqual(True, beacon.is_point_in_range(4, 4))
        self.assertEqual(False, beacon.is_point_in_range(3, 6))
        self.assertEqual(False, beacon.is_point_in_range(6, 3))
        self.assertEqual(False, beacon.is_point_in_range(3, 0))
        self.assertEqual(False, beacon.is_point_in_range(0, 3))

    def test_beacon_in_range(self):
        beacon_1 = Beacon(1, 3, 2)
        beacon_2 = Beacon(4, 5, 3)
        beacon_3 = Beacon(4, 10, 2)
        self.assertEqual(True, beacon_1.is_beacon_in_range(beacon_2))
        self.assertEqual(True, beacon_2.is_beacon_in_range(beacon_1))
        self.assertEqual(True, beacon_2.is_beacon_in_range(beacon_3))
        self.assertEqual(False, beacon_1.is_beacon_in_range(beacon_3))
        self.assertEqual(False, beacon_3.is_beacon_in_range(beacon_1))


class TestBeaconGroup(unittest.TestCase):
    def test_init(self):
        beacon = Beacon(1, 1, 1)
        group_1 = BeaconGroup()
        group_2 = BeaconGroup(beacon)
        self.assertEqual(len(group_1.beacons), 0)
        self.assertEqual(len(group_2.beacons), 1)

    def test_add(self):
        beacon_1 = Beacon(1, 3, 2)
        beacon_2 = Beacon(4, 5, 3)
        beacon_3 = Beacon(4, 10, 2)
        group = BeaconGroup()
        group.add(beacon_1)
        self.assertEqual(len(group.beacons), 1)
        group.add(beacon_2)
        self.assertEqual(len(group.beacons), 2)
        group.add(beacon_3)
        self.assertEqual(len(group.beacons), 3)
        self.assertEqual(True, beacon_2 in group.beacons)

    @staticmethod
    def create_group() -> BeaconGroup:
        group = BeaconGroup()
        group.add(Beacon(1, 3, 2))
        group.add(Beacon(4, 5, 3))
        group.add(Beacon(4, 10, 2))
        return group

    def test_point_in_range(self):
        group = self.create_group()
        self.assertEqual(True, group.is_point_in_range(2, 3))
        self.assertEqual(True, group.is_point_in_range(2, 4))
        self.assertEqual(True, group.is_point_in_range(4, 9))
        self.assertEqual(True, group.is_point_in_range(4, 8))
        self.assertEqual(False, group.is_point_in_range(3, 1))
        self.assertEqual(False, group.is_point_in_range(3, 8))
        self.assertEqual(False, group.is_point_in_range(1, 6))

    def test_beacon_in_range(self):
        group = self.create_group()
        self.assertEqual(True, group.is_beacon_in_range(Beacon(1, 3, 2)))
        self.assertEqual(True, group.is_beacon_in_range(Beacon(2, 3, 1)))
        self.assertEqual(True, group.is_beacon_in_range(Beacon(9, 5, 2)))
        self.assertEqual(True, group.is_beacon_in_range(Beacon(5, 13, 2)))
        self.assertEqual(False, group.is_beacon_in_range(Beacon(5, 1, 1)))
        self.assertEqual(False, group.is_beacon_in_range(Beacon(100, 100, 20)))


class TestWorld(unittest.TestCase):
    def test_world_from_task(self):
        world = World()
        world.add(Beacon(6, 11, 4))
        world.add(Beacon(8, 17, 3))
        world.add(Beacon(19, 19, 2))
        world.add(Beacon(19, 11, 4))
        world.add(Beacon(15, 7, 6))
        world.add(Beacon(12, 19, 4))
        self.assertEqual(len(world.groups), 2)
        g1 = world.groups[0]
        g2 = world.groups[1]
        if len(g1.beacons) > len(g2.beacons):
            g1, g2 = g2, g1
        self.assertEqual(len(g1.beacons), 1)
        self.assertEqual(len(g2.beacons), 5)
        self.assertEqual(g1.beacons[0].position_x, 19)
        self.assertEqual(g1.beacons[0].position_y, 19)
        point_ok_1 = (10, 19)
        point_ok_2 = (19, 14)
        point_nok_1 = (1, 1)
        point_nok_2 = (12, 14)
        point_2nd_group_1 = (19, 19)
        point_2nd_group_2 = (20, 20)
        self.assertEqual(world.is_there_path(point_ok_1, point_ok_2), True)
        self.assertEqual(world.is_there_path(point_ok_2, point_ok_1), True)
        self.assertEqual(world.is_there_path(point_2nd_group_1, point_2nd_group_2), True)
        self.assertEqual(world.is_there_path(point_ok_1, point_2nd_group_1), False)
        self.assertEqual(world.is_there_path(point_2nd_group_2, point_ok_2), False)
        self.assertEqual(world.is_there_path(point_nok_1, point_ok_1), False)
        self.assertEqual(world.is_there_path(point_ok_2, point_nok_2), False)


if __name__ == '__main__':
    unittest.main()
