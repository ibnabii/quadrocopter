from quadrocopter import Beacon, World


class BeaconString(Beacon):
    def __init__(self, string: str):
        super().__init__(*[int(item) for item in string.split()])


if __name__ == '__main__':
    number_of_beacons = int(input("Podaj liczbę nadajników: "))
    world = World()
    for _ in range(number_of_beacons):
        world.add(BeaconString(input("Podaj 3 liczby: x, y, zasięg nadajnika, oddzielone spacjami np. '2 3 1': ")))
    point_1 = [int(item) for item in input("Podaj współrzędne punktu początkowego: ").split()]
    point_2 = [int(item) for item in input("Podaj współrzędne punktu końcowego: ").split()]
    if world.is_there_path(tuple(point_1), tuple(point_2)):
        print("bezpieczny przelot jest możliwy")
    else:
        print("bezpieczny przelot nie jest możliwy")
