import matplotlib
import numpy as np

# Параметры для параллельной линии с отклонениями
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')  # Используем TkAgg для визуализации
from collections import defaultdict

# Данные
data = [[1, 200], [2, 117], [5, 70], [7, 51], [10, 37], [12, 30], [15, 24], [20, 20], [30, 15], [60, 8]]
data2 = [0, 1, 4, 12, 28, 44, 64, 91, 100, 100]
x_indices = range(len(data))
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
plt.plot(x_indices, y_avg, color='b', label="широковещательное сообщение")
plt.ylabel('служебных сообщений в секунду')

ax2 = plt.twinx()
ax2.plot(x_indices, data2, color='r', label='Потерено пакетов %')
ax2.plot(0, -1, color='b', label='сообщений в секунду')
ax2.tick_params(axis='y', labelcolor='r')
plt.ylim(0, 100)
plt.xticks(x_indices, x_avg)
# Добавление подписей
plt.title('Корреляция частоты обновления сети с риском потери пакета')
plt.xlabel('Количество узлоов')
plt.ylabel('Потерено пакетов %')
ax2.legend("Aa")

plt.legend()
plt.grid(True)

# Показ графика
plt.show()
