import numpy as np
import matplotlib.pyplot as plt

# Константы
d = 100  # Расстояние между передатчиком и приёмником в метрах
c = 3e8  # Скорость света в вакууме (м/с)
f_0 = 2.4e9  # Базовая частота (например, 2.4 ГГц для Wi-Fi)

# Диапазон частот
delta_f = np.linspace(-100e6, 100e6, 500)  # Изменение частоты от -100 МГц до 100 МГц
f = f_0 + delta_f  # Полная частота

# Рассчёт затухания сигнала
LFS_dB = 20 * np.log10((4 * np.pi * d * f) / c)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(delta_f / 1e6, LFS_dB, label=f"Расстояние d = {d} м")
plt.xlabel("Частотный сдвиг Δf (МГц)")
plt.ylabel("Затухание сигнала LFS (дБ)")
plt.title("Зависимость затухания сигнала от частотного сдвига Δf")
plt.legend()
plt.grid(True)
plt.show()
