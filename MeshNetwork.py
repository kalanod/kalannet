import math
import random
import time

import numpy as np
from matplotlib import pyplot as plt


class MeshNetwork:
    def get_dist(self, sender, address):
        return math.sqrt(
            (sender.position[0] - address.position[0]) ** 2 + (sender.position[1] - address.position[1]) ** 2)

    def __init__(self):
        self.drones = {}

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

    def new_message(self, message):
        for i in self.drones:
            if self.get_dist(message.sender, self.drones[i]) <= message.range and \
                    i.drone_id != message.sender.drone_id:
                self.drones[i].receive_message(message)