import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt 

def idf_curve(t, A, B, C):
    """
    Fungsi kurva Intensitas-Durasi-Frekuensi (IDF).
    I(t) = A / (t + B)^C

    Args:
        t (array-like): Durasi hujan dalam menit.
        A (float): Parameter A dari kurva IDF.
        B (float): Parameter B dari kurva IDF.
        C (float): Parameter C dari kurva IDF.

    Returns:
        array-like: Intensitas hujan dalam mm/jam.
    """
    return A / ((t + B) ** C)

# Durasi hujan dalam menit
durations_minutes = np.array([5, 10, 30, 60, 120]) 
intensities_mm_per_hour = np.array([
    2767.5826156406233, 
    1383.7913078203117, 
    461.26376927343722, 
    230.63188463671861, 
    115.3159423183593   
])

p0 = [1000.0, 5.0, 0.5] 

try:
    popt, pcov = curve_fit(idf_curve, durations_minutes, intensities_mm_per_hour, p0=p0)

    # Ekstrak parameter A, B, C yang optimal
    A_optimal, B_optimal, C_optimal = popt

    print(f"Fitting Kurva IDF Berhasil!")
    print(f"Parameter Optimal (A, B, C):")
    print(f"A = {A_optimal:.10f}")
    print(f"B = {B_optimal:.10f}")
    print(f"C = {C_optimal:.10f}")

    plt.figure(figsize=(10, 6))
    plt.scatter(durations_minutes, intensities_mm_per_hour, label='Data dari Excel', color='red', marker='o')

    t_fit = np.linspace(min(durations_minutes), max(durations_minutes), 100)
    intensities_fit = idf_curve(t_fit, A_optimal, B_optimal, C_optimal)
    plt.plot(t_fit, intensities_fit, label=f'Kurva Fitting: I(t) = {A_optimal:.2f} / (t + {B_optimal:.2f})^{C_optimal:.2f}', color='blue')

    plt.title('Fitting Kurva IDF')
    plt.xlabel('Durasi (menit)')
    plt.ylabel('Intensitas (mm/jam)')
    plt.legend()
    plt.grid(True)
    plt.show()

except RuntimeError as e:
    print(f"Error saat melakukan fitting: {e}")
    print("Coba sesuaikan tebakan awal (p0) atau periksa data input Anda.")
except Exception as e:
    print(f"Terjadi kesalahan lain: {e}")

