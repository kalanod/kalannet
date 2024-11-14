import numpy as np
import matplotlib.pyplot as plt

# Заданные параметры
P_r = 1e-9  # Мощность на приёмнике (Вт)
P_t = 1e-3  # Мощность на передатчике (Вт)
G_r = 10  # Усиление приёмной антенны (коэффициент)
f = 2.4e9  # Частота сигнала (Гц)
c = 3e8  # Скорость света (м/с)

# Длина волны
lambda_ = c / f

# Диапазон расстояний (от 1 км до 20 км)
distances = np.linspace(1e3, 2e4, 100)

# Вычисляем требуемое усиление антенны передатчика G_t для каждого расстояния (первый график)
G_t = (P_r * (4 * np.pi * distances) ** 2) / (P_t * G_r * lambda_ ** 2)
G_t_db = 10 * np.log10(G_t)  # Усиление в дБ

# Разделяем массив расстояний на 5 равных частей
n_sections = 5
section_size = len(distances) // n_sections
G_t_div_sections_db = np.zeros_like(G_t_db)

# Вычисляем усиление для расстояний в каждой секции с делением на 1, 2, 3, 4 и 5 соответственно
for i in range(n_sections):
    start_idx = i * section_size
    end_idx = start_idx + section_size if i < n_sections - 1 else len(distances)
    divided_distances = distances[start_idx:end_idx] / (i + 1)

    # Рассчитываем усиление для текущей секции
    G_t_section = (P_r * (4 * np.pi * divided_distances) ** 2) / (P_t * G_r * lambda_ ** 2)
    G_t_div_sections_db[start_idx:end_idx] = 10 * np.log10(G_t_section)

# Выводим разницу значений для 5 точек
selected_distances = np.linspace(1e3, 2e4, 5)
selected_G_t_db = 10 * np.log10((P_r * (4 * np.pi * selected_distances) ** 2) / (P_t * G_r * lambda_ ** 2))
selected_G_t_div_sections_db = np.interp(selected_distances, distances, G_t_div_sections_db)
differences_db = selected_G_t_div_sections_db - selected_G_t_db

# Выводим разницу значений в консоль
print("Расстояние (км) | Разница усилений (дБ)")
print("---------------------------------------")
for d, diff in zip(selected_distances, differences_db):
    print(f"{d / 1e3:.2f} км       | {diff:.2f} дБ")

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(distances / 1e3, G_t_db, label="Исходное усиление", color="blue")
plt.plot(distances / 1e3, G_t_div_sections_db, label="Усиление с делением на секции", color="orange")
plt.xscale("log")  # Логарифмическая шкала по расстоянию
plt.xlabel("Расстояние, км (логарифмическая шкала)")
plt.ylabel("Требуемое усиление антенны передатчика, G_t (дБ)")
plt.title("Зависимость усиления антенны передатчика от расстояния")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()
