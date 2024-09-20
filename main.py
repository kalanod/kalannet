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
    network.add_drone(Drone(i, Drone.Coordinates(*position), 100, network))
network.drones[0].connect()
network.drones[1].connect()
print(network.drones[0].routing_table)
