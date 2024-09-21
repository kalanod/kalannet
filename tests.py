# Добавление дронов в сеть
import random

from Drone import Drone
from MeshNetwork import MeshNetwork

network = MeshNetwork(1)
rad = 50
res = []
for i in range(15):
    tmp = []
    for i in range(10):
        print("test", i, "/ 50")
        position = (random.uniform(0, 100), random.uniform(0, 100))
        network.add_drone(Drone(i, Drone.Coordinates(*position), rad, network))
        network.update()
        sum_bands = network.sum_bands()
        res.append([num, sum_bands])
        network.clear()
# res.sort(key=lambda x: x[0])
print(res)
# network.add_drone(Drone(1, Drone.Coordinates(50, 0), 60, network))
# network.add_drone(Drone(2, Drone.Coordinates(100, 0), 60, network))
# network.add_drone(Drone(3, Drone.Coordinates(150, 0), 60, network))
# network.drones[0].connect()
# network.drones[1].connect()
# network.drones[2].connect()
# network.drones[3].connect()
# print(network.drones[0].routing_table)
# print(network.drones[1].routing_table)
# print(network.drones[2].routing_table)
# print(network.drones[3].routing_table)
