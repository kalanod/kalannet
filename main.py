import math
import random
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('TkAgg')


class Message:
    def __init__(self, channel, sender, address, text):
        self.id = str(sender.drone_id) + str(random.randint(0, 99999999))
        self.channel = channel
        self.sender = sender
        self.address = address
        self.text = text
        self.range = sender.range


class Drone:
    def __init__(self, drone_id, position, range, area):
        self.drone_id = drone_id
        self.position = position
        self.range = range
        self.is_connected = False
        self.area = area
        self.memory = []

    def connect(self):
        self.area.sendMessage(Message(1, self, 0, "hi"))
        self.connected = True
        print(f"Drone {self.drone_id} connected to the network.")

    def disconnect(self):
        self.connected = False
        print(f"Drone {self.drone_id} disconnected from the network.")

    def send_message(self, message):
        if self.connected:
            signal = self.ofdm_modulation(message)
            print(f"Drone {self.drone_id} sending message: {message}")
            network.broadcast_signal(self, signal)

    def receive_message(self, message):
        if message.address != self.drone_id and \
                message.id not in self.memory:
            self.send_message(message)
        print(f"Drone {self.drone_id} received message: {message}")

    def ofdm_modulation(self, message):
        bits = ''.join(format(ord(i), '08b') for i in message)
        symbols = np.array([int(bit) for bit in bits])
        carriers = np.fft.ifft(symbols)
        return carriers


class MeshNetwork:
    def get_dist(self, sender, address):
        return math.sqrt(
            (sender.position[0] - address.position[0]) ** 2 + (sender.position[1] - address.position[1]) ** 2)

    def __init__(self):
        self.drones = {}

    def sendMessage(self, message):
        for i in self.drones:
            if self.get_dist(message.sender, self.drones[i]) <= message.range and \
                    i.drone_id != message.sender.drone_id:
                self.drones[i].receive_message(message)

    def add_drone(self, drone):
        self.drones[drone.drone_id] = drone
        print(f"Drone {drone.drone_id} added to the network.")

    def remove_drone(self, drone):
        self.drones.pop(drone.drone_id)
        print(f"Drone {drone.drone_id} removed from the network.")

    def connect_random_drone(self):
        if self.drones:
            drone = random.choice(self.drones)
            if not drone.connected:
                drone.connect()

    def disconnect_random_drone(self):
        if self.drones:
            drone = random.choice(self.drones)
            if drone.connected:
                drone.disconnect()

    def simulate_network_activity(self, duration=10):
        start_time = time.time()
        while time.time() - start_time < duration:
            action = random.choice(['connect', 'disconnect', 'send_message'])
            if action == 'connect':
                self.connect_random_drone()
            elif action == 'disconnect':
                self.disconnect_random_drone()
            elif action == 'send_message':
                drone = random.choice(self.drones)
                if drone.connected:
                    drone.send_message("Test message", self)
            self.visualize_network()
            time.sleep(random.uniform(0.5, 2))

    def broadcast_signal(self, sender_drone, signal):
        for drone in self.drones:
            if drone != sender_drone and self.is_in_range(sender_drone, drone):
                drone.receive_message("Test message")

    def is_in_range(self, drone1, drone2):
        dist = np.linalg.norm(np.array(drone1.position) - np.array(drone2.position))
        return dist <= drone1.range

    def visualize_network(self):
        plt.figure(figsize=(8, 8))
        for drone in self.drones:
            if drone.connected:
                plt.scatter(*drone.position, c='green',
                            label=f'Drone {drone.drone_id}' if drone == self.drones[0] else "")
                circle = plt.Circle(drone.position, drone.range, color='green', fill=False, linestyle='--', alpha=0.5)
            else:
                plt.scatter(*drone.position, c='red',
                            label=f'Drone {drone.drone_id}' if drone == self.drones[0] else "")
                circle = plt.Circle(drone.position, drone.range, color='red', fill=False, linestyle='--', alpha=0.5)
            plt.gca().add_patch(circle)
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.title("Drone Network Visualization")
        plt.legend(loc='upper right')
        plt.draw()
        plt.pause(0.1)
        plt.clf()


# Пример использования

network = MeshNetwork()

# Добавление дронов в сеть
for i in range(5):
    position = (random.uniform(0, 100), random.uniform(0, 100))
    drone = Drone(drone_id=i, position=position, range_=50)
    network.add_drone(drone)

# Запуск симуляции на 10 секунд
plt.ion()
network.simulate_network_activity(duration=10)
plt.ioff()
plt.show()
