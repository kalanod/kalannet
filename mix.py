import numpy as np
from sympy import symbols, Eq, solve

# Данные задачи
C1 = np.array([0, 0, 1, 1, 1, 0, 1, 1])  # C1 = 00111011
C2 = np.array([0, 1, 1, 0, 0, 0, 1, 0])  # C2 = 01100010

# Определяем символические переменные для ключа K
k = symbols('k0 k1 k2 k3 k4 k5 k6 k7', integer=True)
K = np.array(k)

# Рассчитываем M1 (M1 = C1 XOR K)
M1 = np.array([C1[i] ^ K[i] for i in range(8)])

# Выполняем циклический сдвиг вправо для M1, чтобы получить M2
M2 = np.roll(M1, 1)  # Циклический сдвиг вправо

# Уравнения для нахождения ключа: C2 = M2 XOR K
equations = [Eq(C2[i], M2[i] ^ K[i]) for i in range(8)]

# Решаем систему уравнений для K
solution = solve(equations, k)

# Выводим решение
print("Решение для K:", solution)

# Если нужно вычислить количество единиц в ключе K
if solution:
    K_values = np.array([solution[k[i]] for i in range(8)], dtype=int)
    print("Ключ K:", K_values)
    print("Число единиц в ключе K:", np.sum(K_values))
