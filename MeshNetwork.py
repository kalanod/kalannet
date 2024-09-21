import math
import random
import threading
import time

from matplotlib import pyplot as plt


class MeshNetwork:
    def get_dist(self, sender, address):
        return math.sqrt(
            (sender.position.x - address.position.x) ** 2 + (sender.position.y - address.position.y) ** 2)

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
                    self.drones[i].drone_id != message.sender.drone_id:
                self.drones[i].receive_message(message)

    def update_drone_coordinates(self, selected_drone, x, y):
        self.drones[selected_drone].position.x = x
        self.drones[selected_drone].position.y = y

    def update_drone_radius(self, drone_id, drone_radius):
        self.drones[drone_id].range = drone_radius

    def start_background_task(self):
        """Запускает фоновый процесс, который проходит по дронам и вызывает нужные методы."""
        self.stop_task = False  # Переменная для остановки потока
        self.task_thread = threading.Thread(target=self.background_task)
        self.task_thread.start()

    def stop_background_task(self):
        """Останавливает фоновый процесс."""
        self.stop_task = True
        self.task_thread.join()  # Ожидаем завершения потока

    def background_task(self):
        """Задача, выполняемая в фоновом режиме, которая проходит по каждому дрону и вызывает методы."""
        while not self.stop_task:
            # Проход по всем дронам
            for drone_id in self.drones:
                drone = self.drones[drone_id]  # Предполагается, что network.drones содержит объекты дронов
                drone.routing_table.clear(drone_id)
                drone.send_message(-1, 0, drone_id)

            time.sleep(1)  # Задержка между проходами, чтобы не перегружать процессор

    # Инициализация интерфейса
