import csv
import os

def save_to_csv(data, file_path):
    """Menyimpan data ke file CSV."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Buat folder jika belum ada
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["No", "Nama Kampus", "Sinta score"])
        writer.writerows(data)
    print(f"Data berhasil disimpan di {file_path}")
