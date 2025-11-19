import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

#ganti 
NAMA_FILE_CSV = 'PRD_FIXED.csv' 
KOLOM_X = 'time'
KOLOM_Y = 'intensity'

# Judul dan label untuk grafik
JUDUL_GRAFIK = 'Peaked Rainfall Distribution'
LABEL_X = 'Waktu (detik)' 
LABEL_Y = 'Intensitas (mm/jam)'


# luas area perhitungan
TOTAL_AREA_M2 = 113293415.29 
# -----------------------------------------------


def buat_grafik_dan_hitung_volume():
    try:
        # 1. baca dari csv
        print(f"Membaca file data '{NAMA_FILE_CSV}'...")
        data = pd.read_csv(NAMA_FILE_CSV)
        
        # ganti nama kolom (opsional)
        if 'intensity' in data.columns and KOLOM_Y not in data.columns:
            data = data.rename(columns={'intensity': KOLOM_Y})
            
        if KOLOM_X not in data.columns or KOLOM_Y not in data.columns:
            print(f"Error: Pastikan file CSV Anda memiliki kolom bernama '{KOLOM_X}' dan '{KOLOM_Y}'.")
            print(f"Kolom yang ada: {data.columns.tolist()}")
            sys.exit(1)
            
        x_values = data[KOLOM_X]
        y_values = data[KOLOM_Y]
        print("Data berhasil dimuat.")

        # 3. luas area dan volume
        # -----------------------------------------------------------------
        print("\n" + "="*50)
        print("HASIL PERHITUNGAN VERIFIKASI SISI A (INPUT HUJAN)")
        
        # area under curve
        auc_mm_hr_s = np.trapz(y_values, x_values)
        print(f"Langkah 1: AUC (Intensitas * Waktu) = {auc_mm_hr_s:,.2f} [mm/jam * s]")
        
        # konversi satuan
        # (mm/jam * s) / (3600 s/jam) = mm
        total_kedalaman_mm = auc_mm_hr_s / 3600.0
        print(f"Langkah 2: Total Kedalaman Hujan     = {total_kedalaman_mm:,.4f} [mm]")
        
        # konversi satuan
        # (mm / 1000 mm/m) * (Total Area m^2) = m^3
        total_volume_m3 = (total_kedalaman_mm / 1000.0) * TOTAL_AREA_M2
        print(f"Langkah 3: TOTAL VOLUME (SISI A)   = {total_volume_m3:,.2f} [m³]")
        print("="*50 + "\n")
        # -----------------------------------------------------------------

        print("Membuat grafik...")
        plt.figure(figsize=(12, 8))
        
        # grafik intensitas
        plt.plot(x_values, y_values, linestyle='-', marker=None, color='blue', label='Intensitas Hujan')
        
        # arsir area under curve
        plt.fill_between(x_values, y_values, color='lightblue', alpha=0.5, 
                         label=f'AUC = {auc_mm_hr_s:,.2f} (mm/jam*s)')

        # judul + tabel keterangan
        judul_lengkap = (
            f"{JUDUL_GRAFIK}\n"
            f"Total Kedalaman (Python): {total_kedalaman_mm:,.4f} mm\n"
            f"Total Volume (Python): {total_volume_m3:,.2f} m³"
        )
        plt.title(judul_lengkap, fontsize=16)
        
        plt.xlabel(LABEL_X, fontsize=12)
        plt.ylabel(LABEL_Y, fontsize=12)
        
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        
        # save gambar grafik
        nama_file_output = f"HASIL_{JUDUL_GRAFIK}.png"
        plt.savefig(nama_file_output)
        print(f"Grafik selesai. Disimpan sebagai '{nama_file_output}'")
        # plt.show() # Tampilkan jika Anda mau

    except FileNotFoundError:
        print(f"Error: File '{NAMA_FILE_CSV}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi error: {e}")

# run fungsi main
if __name__ == "__main__":
    buat_grafik_dan_hitung_volume()

