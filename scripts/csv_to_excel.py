import pandas as pd
import os

# Baca data dari file CSV
csv_file_path = "data/daftar_ptn_sainsdata.csv"
df = pd.read_csv(csv_file_path)

# Buat folder 'fix' jika belum ada
output_folder = "fix"
os.makedirs(output_folder, exist_ok=True)

# Tentukan path untuk file Excel output
excel_file_path = os.path.join(output_folder, "daftar_ptn_sainsdata.xlsx")

# Simpan data ke file Excel
df.to_excel(excel_file_path, index=False)

print(f"Data berhasil disimpan di {excel_file_path}")