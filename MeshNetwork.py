import math
import random
import threading
import time


class MeshNetwork:
    def get_dist(self, sender, address):
        return math.sqrt(
            (sender.position.x - address.position.x) ** 2 + (sender.position.y - address.position.y) ** 2)

    def __init__(self, silent=False):
        self.drones = {}
        self.silent = silent

    def add_drone(self, drone):
        self.drones[drone.drone_id] = drone
        self.drones[drone.drone_id].connect()
        if not self.silent:
            print(f"Drone {drone.drone_id} added to the network.")

    def remove_drone(self, drone):
        self.drones.pop(drone.drone_id)
        if not self.silent:
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

    def update(self):
        for drone_id in self.drones:
            drone = self.drones[drone_id]  # Предполагается, что network.drones содержит объекты дронов
            drone.routing_table.clear(drone_id)
            drone.send_message(-1, 0, drone_id)

    # Инициализация интерфейса
    def connected(self, drone1, drone2):
        return drone2 in self.drones[drone1].routing_table.table

    def length(self, drone1, drone2):
        return self.drones[drone1].routing_table.table[drone2][0].length


    def sum_bands(self):
        res = 0
        for i in self.drones:
            res += len(self.drones[i].routing_table.table) - 2
        return res

    def clear(self):
        self.drones = {}
