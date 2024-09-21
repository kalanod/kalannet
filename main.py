import tkinter as tk
from tkinter import simpledialog
from Drone import Drone
from MeshNetwork import MeshNetwork

network = MeshNetwork()

class DroneNetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone Network Visualization")
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.drone_radius = 50  # Увеличен радиус дронов
        self.drones = {}
        self.lines = {}  # Для хранения линий между дронами
        self.drone_count = 0
        self.selected_drone = None
        self.is_dragging = False

        # Связываем события
        self.canvas.bind("<Button-1>", self.on_left_click)  # Левый клик для добавления/удаления дронов
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release)  # Для обработки завершения клика
        self.canvas.bind("<Button-3>", self.on_right_click)  # Правый клик для отправки сообщения
        self.canvas.bind("<B1-Motion>", self.on_drag)  # Перемещение дронов
        self.canvas.bind("<MouseWheel>", self.on_scroll)  # Регулировка зоны действия

    def on_left_click(self, event):
        x, y = event.x, event.y
        self.is_dragging = False  # По умолчанию не перетаскиваем
        self.selected_drone = None  # Сбрасываем выбор

        for drone_id, (drone_circle, drone_range, label) in self.drones.items():
            if self.is_within_circle(x, y, *self.canvas.coords(drone_circle)):
                # Найден дрон для перетаскивания
                self.selected_drone = drone_id
                return  # Если дрон найден, выходим

        # Если на месте клика нет дрона, добавляем новый
        self.drone_count += 1
        drone_circle = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue")  # Дрон увеличен в 2 раза
        drone_range = self.canvas.create_oval(x-self.drone_radius, y-self.drone_radius, x+self.drone_radius, y+self.drone_radius, outline="blue")
        label = self.canvas.create_text(x, y-15, text=f"ID: {self.drone_count}", fill="black")  # Подпись ID над дроном

        self.drones[self.drone_count] = (drone_circle, drone_range, label)

        # Вызов функции бэкенда для добавления дрона
        network.add_drone(Drone(self.drone_count, Drone.Coordinates(x, y), self.drone_radius, network))
        network.drones[self.drone_count].connect()

        # Обновляем отображение связей между дронами
        self.update_connections()

    def on_left_release(self, event):
        # Если мышь не перемещалась (is_dragging == False), это был клик для удаления
        if self.selected_drone is not None and not self.is_dragging:
            # Удаление дрона по отпусканию кнопки
            drone_circle, drone_range, label = self.drones[self.selected_drone]
            self.canvas.delete(drone_circle)
            self.canvas.delete(drone_range)
            self.canvas.delete(label)
            del self.drones[self.selected_drone]
            # Удаление связей
            self.remove_connections(self.selected_drone)
        self.selected_drone = None  # Сбрасываем выбранный дрон

    def on_drag(self, event):
        if self.selected_drone is not None:
            # Если началось движение, включаем флаг перетаскивания
            self.is_dragging = True

            # Перемещаем выбранный дрон
            drone_circle, drone_range, label = self.drones[self.selected_drone]
            x, y = event.x, event.y
            self.canvas.coords(drone_circle, x-10, y-10, x+10, y+10)  # Дрон увеличен в 2 раза
            self.canvas.coords(drone_range, x-self.drone_radius, y-self.drone_radius, x+self.drone_radius, y+self.drone_radius)
            self.canvas.coords(label, x, y-15)  # Обновляем положение подписи

            # Обновляем данные в бэкенде
            network.update_drone_coordinates(self.selected_drone, x, y)

            # Обновляем отображение связей между дронами
            self.update_connections()


    def on_right_click(self, event):
        x, y = event.x, event.y
        for drone_id, (drone_circle, _, _) in self.drones.items():
            if self.is_within_circle(x, y, *self.canvas.coords(drone_circle)):
                # Открываем диалоговое окно для ввода ID получателя сообщения
                recipient_id = simpledialog.askinteger("Send Message", "Enter the ID of the recipient:")
                if recipient_id is not None:
                    print(f"Sending message from Drone {drone_id} to Drone {recipient_id}")
                    network.drones[drone_id].send_message(recipient_id, 5, "hi")
                return

    def on_scroll(self, event):
        # Регулируем зону действия дрона по наведению колесика мыши
        x, y = event.x, event.y
        for drone_id, (drone_circle, drone_range, _) in self.drones.items():
            if self.is_within_circle(x, y, *self.canvas.coords(drone_circle)):
                # Увеличиваем/уменьшаем радиус зоны действия
                if event.delta > 0:
                    self.drone_radius += 5
                else:
                    self.drone_radius = max(5, self.drone_radius - 5)

                # Обновляем отображение зоны действия
                self.canvas.coords(drone_range, x-self.drone_radius, y-self.drone_radius, x+self.drone_radius, y+self.drone_radius)

                # Обновляем данные в бэкенде
                network.update_drone_radius(drone_id, self.drone_radius)

                # Обновляем отображение связей между дронами
                self.update_connections()
                return

    def update_connections(self):
        """Обновляет линии соединений между дронами на основе таблицы маршрутизации."""
        # Удаляем все существующие линии
        for line in self.lines.values():
            self.canvas.delete(line)
        self.lines.clear()

        # Рисуем новые линии
        for drone_id, (drone_circle, _, _) in self.drones.items():
            x0, y0, x1, y1 = self.canvas.coords(drone_circle)
            center_x = (x0 + x1) / 2
            center_y = (y0 + y1) / 2

            routing_table = network.drones[drone_id].routing_table.table
            for route in routing_table.values():
                for r in route:
                    if r.address in self.drones:
                        target_drone_circle, _, _ = self.drones[r.address]
                        tx0, ty0, tx1, ty1 = self.canvas.coords(target_drone_circle)
                        target_x = (tx0 + tx1) / 2
                        target_y = (ty0 + ty1) / 2

                        # Рисуем линию между дронами
                        line = self.canvas.create_line(center_x, center_y, target_x, target_y, fill="green", dash=(4, 2))
                        self.lines[(drone_id, r.address)] = line

    def remove_connections(self, drone_id):
        """Удаляет все линии, связанные с удаленным дроном."""
        for (d_id, target_id) in list(self.lines.keys()):
            if d_id == drone_id or target_id == drone_id:
                self.canvas.delete(self.lines[(d_id, target_id)])
                del self.lines[(d_id, target_id)]

    def is_within_circle(self, x, y, x0, y0, x1, y1):
        """Проверяет, находится ли точка (x, y) внутри круга, заданного координатами углов (x0, y0) и (x1, y1)."""
        radius = (x1 - x0) / 2
        center_x, center_y = (x0 + x1) / 2, (y0 + y1) / 2
        return (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2

root = tk.Tk()
app = DroneNetworkApp(root)
network.start_background_task()
root.protocol("WM_DELETE_WINDOW", lambda: [network.stop_background_task(), root.destroy()])

root.mainloop()
