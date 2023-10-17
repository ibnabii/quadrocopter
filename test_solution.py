import unittest

from solution import BeaconString


class TestBeaconString(unittest.TestCase):
    def test_init(self):
        beacon = BeaconString("2 5 6")
        self.assertEqual(beacon.position_x, 2)
        self.assertEqual(beacon.position_y, 5)
        self.assertEqual(beacon.radius, 6)
        beacon = BeaconString("25 125 3")
        self.assertEqual(beacon.position_x, 25)
        self.assertEqual(beacon.position_y, 125)
        self.assertEqual(beacon.radius, 3)


if __name__ == '__main__':
    unittest.main()
