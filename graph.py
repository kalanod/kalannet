import matplotlib
import numpy as np

# Параметры для параллельной линии с отклонениями
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')  # Используем TkAgg для визуализации
from collections import defaultdict

# Данные
data = [[0, 0], [1, 6], [2, 24], [3, 49], [4, 84], [5, 137], [6, 204], [7, 277], [8, 402], [9, 546]]

# Словарь для хранения сумм значений y и количества элементов для каждого x
x_to_y_values = defaultdict(list)

# Заполнение словаря
for x, y in data:
    x_to_y_values[x].append(y)

# Средние значения для каждого x
x_avg = sorted(x_to_y_values.keys())
y_avg = [sum(y_values)/len(y_values) for y_values in [x_to_y_values[x] for x in x_avg]]

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(x_avg, y_avg, marker='o', color='b')

# Добавление подписей
plt.title('Среднее количество связей от узлов')
plt.xlabel('Количество узлов')
plt.ylabel('Количество связей')
plt.legend()
plt.grid(True)

# Показ графика
plt.show()
