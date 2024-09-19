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

# Запуск симуляции на 10 секунд
plt.ion()
network.simulate_network_activity(duration=10)
plt.ioff()
plt.show()
