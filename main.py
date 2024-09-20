import math
import random
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from Drone import Drone
from MeshNetwork import MeshNetwork

matplotlib.use('TkAgg')

network = MeshNetwork()

# Добавление дронов в сеть
for i in range(5):
    position = (random.uniform(0, 100), random.uniform(0, 100))
network.add_drone(Drone(0, Drone.Coordinates(0, 0), 60, network))
network.add_drone(Drone(1, Drone.Coordinates(50, 0), 60, network))
network.add_drone(Drone(2, Drone.Coordinates(100, 0), 60, network))
network.drones[0].connect()
network.drones[1].connect()
network.drones[2].connect()
print(network.drones[0].routing_table)
print(network.drones[1].routing_table)
print(network.drones[2].routing_table)
