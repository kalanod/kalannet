import numpy as np
import matplotlib.pyplot as plt

# --------------- Параметры системы ---------------
# Длительность одного OFDM-символа (без циклического префикса)
T_sym = 1e-3  # сек.
f_c = 2000  # Частота несущей для passband-модуляции, Гц
fs = 100000  # Частота дискретизации, Гц

# Параметры FFT/OFDM
N_sub = 16  # Количество поднесущих (16-QAM по 16 поднесущим)
N_fft = int(T_sym * fs)  # Длина IFFT (число отсчетов на символ). Здесь применяется oversampling.
N_OFDM = 5  # Количество OFDM символов (можно менять)

# --------------- Генерация битовой последовательности и маппинг 16-QAM ---------------
# Для 16-QAM 4 бита на символ, всего символов: N_sub * N_OFDM
num_total_symbols = N_sub * N_OFDM
num_bits = num_total_symbols * 4

# Генерируем случайные биты (0 или 1)
bits = np.random.randint(0, 2, num_bits)
print("Битовая последовательность:")
print(bits)

# Gray-мэппинг для 2-битовой группы:
# (0,0)-> -3, (0,1)-> -1, (1,1)-> +1, (1,0)-> +3
mapping = {
    (0, 0): -3,
    (0, 1): -1,
    (1, 1): 1,
    (1, 0): 3
}

# Преобразуем биты в QAM-символы: получаем последовательности I и Q
I_symbols = []
Q_symbols = []
for i in range(num_total_symbols):
    b_I = (bits[4 * i], bits[4 * i + 1])
    b_Q = (bits[4 * i + 2], bits[4 * i + 3])
    I_symbols.append(mapping[b_I])
    Q_symbols.append(mapping[b_Q])

I_symbols = np.array(I_symbols)
Q_symbols = np.array(Q_symbols)
X_symbols = I_symbols + 1j * Q_symbols  # Комплексные 16-QAM символы

# Для удобства преобразуем последовательность в матрицу:
# Каждая строка соответствует одному OFDM-символу, в строке N_sub символов.
X_matrix = X_symbols.reshape(N_OFDM, N_sub)

# --------------- Формирование базband OFDM-сигнала ---------------
# Будем использовать IFFT для каждого OFDM-символа.
# При этом создаем вектор длины N_fft, где первые N_sub бинов заполняются QAM-символами, остальные = 0.
# Используем нормировку 1/sqrt(N_sub) для сохранения мощности.
ofdm_signal_baseband = np.array([])  # Здесь будем аккумулировать все OFDM символы (без циклического префикса)

for i in range(N_OFDM):
    # Создаем вектор в частотной области длины N_fft
    X_freq = np.zeros(N_fft, dtype=complex)
    # Заполняем первые N_sub позиций (можно выбрать и иной план распределения, но здесь просто подряд)
    X_freq[0:N_sub] = X_matrix[i, :]

    # Выполняем обратное БПФ (IFFT)
    x_time = np.fft.ifft(X_freq)  # x_time имеет длину N_fft
    # Нормировка по количеству поднесущих: 1/sqrt(N_sub)
    x_time = x_time / np.sqrt(N_sub)

    # Конкатенируем OFDM-символы воедино
    ofdm_signal_baseband = np.concatenate((ofdm_signal_baseband, x_time))

# Создаем временную ось для базband-сигнала:
total_samples = len(ofdm_signal_baseband)
t_baseband = np.linspace(0, total_samples / fs, total_samples, endpoint=False)

# --------------- Модуляция базband сигнала на несущую (passband) ---------------
# Passband сигнал: s(t) = Re{ x(t) * exp(j2*pi*f_c*t) }
ofdm_signal_passband = np.real(ofdm_signal_baseband * np.exp(1j * 2 * np.pi * f_c * t_baseband))

# --------------- Построение графиков ---------------
plt.figure(figsize=(12, 10))

# График 1. Базband-сигнал (реальная часть)
plt.subplot(3, 1, 1)
plt.plot(t_baseband, np.real(ofdm_signal_baseband), 'b')
plt.title('Базband OFDM-сигнал (реальная часть)')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.grid(True)

# График 2. Базband-сигнал (мнимую часть)
plt.subplot(3, 1, 2)
plt.plot(t_baseband, np.imag(ofdm_signal_baseband), 'r')
plt.title('Базband OFDM-сигнал (мнимой части)')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.grid(True)

# График 3. Передаваемый passband-сигнал
plt.subplot(3, 1, 3)
plt.plot(t_baseband, ofdm_signal_passband, 'k')
plt.title('Передаваемый OFDM passband-сигнал')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.grid(True)

plt.tight_layout()
plt.show()
