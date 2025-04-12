from difflib import Match
from math import log10

import numpy as np
import matplotlib.pyplot as plt

# Given parameters
P_r = 1e-9  # Power at the receiver (W)
P_t = 1e-3  # Power at the transmitter (W)
G_r = 10  # Receiver antenna gain (factor)
f = 2.4e9  # Signal frequency (Hz)
c = 3e8  # Speed of light (m/s)

# Wavelength
lambda_ = c / f

# Distance range (from 1 km to 20 km)
distances = np.linspace(1e3, 2e4, 100)

# Calculate the required transmitter antenna gain G_t for each distance (first plot)
G_t = (P_r * (4 * np.pi * distances) ** 2) / (P_t * G_r * lambda_ ** 2)
G_t_db = 10 * G_t  # Gain in dB

# Divide the distance array into 5 equal sections
n_sections = 5
section_size = len(distances) // n_sections
G_t_div_sections_db = np.zeros_like(G_t_db)

# Energy calculation
# Assuming a fixed data transmission time (1 second for simplicity)
t_tx = 1  # Transmission time in seconds
P_t_adapted = P_t * G_t  # Power adjusted by gain
E_tx = P_t_adapted * t_tx  # Energy in Joules

# Calculate the gain for distances in each section divided by 1, 2, 3, 4, and 5 respectively
for i in range(n_sections):
    start_idx = i * section_size
    end_idx = start_idx + section_size if i < n_sections - 1 else len(distances)
    divided_distances = distances[start_idx:end_idx] / (i + 1)

    # Compute the gain for the current section
    G_t_section = (P_r * (4 * np.pi * divided_distances) ** 2) / (P_t * G_r * lambda_ ** 2) * (i + 1) / 50000 + log10(4000.7 )+  0.1 * (i+1)
    G_t_div_sections_db[start_idx:end_idx] =  G_t_section

# Output the difference for 5 selected points
selected_distances = np.linspace(1e3, 2e4, 5)
selected_G_t_db = 10 * (P_r * (4 * np.pi * selected_distances) ** 2) / (P_t * G_r * lambda_ ** 2)
selected_G_t_div_sections_db = np.interp(selected_distances, distances, G_t_div_sections_db)
differences_db = selected_G_t_div_sections_db - selected_G_t_db


plt.figure(figsize=(10, 6))
plt.plot(distances / 1e3, G_t_div_sections_db, label="Energy (Joules)", color="orange")
plt.xlabel("Distance, km")
plt.ylabel("Energy (Joules/Mb)")
plt.title("Dependence of Transmitter Antenna Gain on Distance")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()
