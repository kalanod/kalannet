import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('TkAgg')

def modulate_signal(A_n, f_n, P_n, t):
    """Модуляция сигнала на несущей."""
    return A_n * np.cos(2 * np.pi * f_n * t + P_n)

def generate_constellation(A_n, P_n, num_points):
    """Генерация созвездия для I и Q компонентов."""
    i_component = A_n * np.cos(P_n)
    q_component = A_n * np.sin(P_n)
    return i_component, q_component

def ofdm_ifft(subcarriers):
    """Выполняем IFFT для поднесущих."""
    time_domain_signal = np.fft.ifft(subcarriers)
    real_part = np.real(time_domain_signal)
    imaginary_part = np.imag(time_domain_signal)
    return real_part, imaginary_part

def dac_interpolate(signal, interpolation_factor):
    """Простое интерполирование (ЦАП)."""
    interpolated_signal = np.interp(
        np.linspace(0, len(signal), len(signal) * interpolation_factor),
        np.arange(len(signal)),
        signal
    )
    return interpolated_signal

def modulate_ofdm_signal(real_part, imaginary_part, carrier_frequency, t):
    """Модуляция OFDM сигнала на несущей."""
    real_modulated = real_part * np.cos(2 * np.pi * carrier_frequency * t)  # Действительная часть на косинус
    imaginary_modulated = imaginary_part * np.sin(2 * np.pi * carrier_frequency * t)  # Мнимая на синус
    return real_modulated + imaginary_modulated  # Сложение для получения результирующего сигнала

def bits_to_signal(bits, mod_scheme='QPSK'):
    """Функция для преобразования битовой последовательности в сигналы на основе выбранной модуляции."""
    symbols = []
    if mod_scheme == 'QPSK':  # Используем QPSK, 2 бита на символ
        for i in range(0, len(bits), 2):
            bit_pair = bits[i:i+2]
            if bit_pair == [0, 0]:
                amplitude, phase = 1, 0
            elif bit_pair == [0, 1]:
                amplitude, phase = 1, np.pi/2
            elif bit_pair == [1, 1]:
                amplitude, phase = 1, np.pi
            elif bit_pair == [1, 0]:
                amplitude, phase = 1, 3*np.pi/2
            symbols.append((amplitude, phase))
    # Можно добавить другие схемы модуляции, например, 16-QAM
    return symbols

# Количество поднесущих
N = 8

# Параметры сигнала
f_n = 5.0
t = np.linspace(0, 1, 1000)  # Шаг времени
carrier_frequency = 10  # Частота несущей
interpolation_factor = 10  # Параметры интерполяции для ЦАП

# Пример битовой последовательности (длина должна быть кратной 2 для QPSK)
bit_sequence = [1, 0, 1, 1, 1, 1, 0, 1]

# Преобразуем биты в сигналы
symbols = bits_to_signal(bit_sequence, mod_scheme='QPSK')

# Генерация OFDM сигнала на основе символов
subcarriers = []
for amplitude, phase in symbols:
    i_component, q_component = generate_constellation(amplitude, phase, len(t))
    subcarriers.append(i_component + 1j * q_component)

# Применение IFFT к поднесущим
real_part, imaginary_part = ofdm_ifft(subcarriers)

# Пропускаем через ЦАП (интерполяция)
real_interpolated = dac_interpolate(real_part, interpolation_factor)
imaginary_interpolated = dac_interpolate(imaginary_part, interpolation_factor)

# Создание временной оси с учётом интерполяции
t_interpolated = np.linspace(0, 1, len(real_interpolated))

# Модуляция OFDM сигнала
ofdm_signal = modulate_ofdm_signal(real_interpolated, imaginary_interpolated, carrier_frequency, t_interpolated)

# Визуализация сигнала
plt.plot(t_interpolated, ofdm_signal)
plt.title('OFDM Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()
