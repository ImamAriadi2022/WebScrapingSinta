import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fungsi untuk membuat direktori jika belum ada
def buat_direktori(nama_direktori):
    if not os.path.exists(nama_direktori):
        os.makedirs(nama_direktori)
        print(f"Direktori '{nama_direktori}' berhasil dibuat.")
    else:
        print(f"Direktori '{nama_direktori}' sudah ada.")

# Fungsi untuk scraping data dari Sinta
def scrape_sinta(page=1):
    url = f"https://sinta.kemdikbud.go.id/affiliations?page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Struktur tabel yang ingin diambil
    data = []
    table = soup.find('table', {'class': 'list-item row mb-4'})  # Tabel data utama
    if table:
        rows = table.find_all('tr')[1:]  # Lewati header
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                # Ambil data sesuai kolom
                rank = cols[0].text.strip()
                name = cols[1].text.strip()
                sinta_score = cols[2].text.strip()
                affiliation_id = cols[1].find('a')['href'].split('=')[-1] if cols[1].find('a') else None
                data.append({
                    'Rank': rank,
                    'Nama Institusi': name,
                    'Sinta Score': sinta_score,
                    'Affiliation ID': affiliation_id
                })
    else:
        print("Tidak dapat menemukan tabel di halaman ini.")
    return data

# Fungsi utama untuk menyimpan data ke CSV
def simpan_data_ke_csv(data, direktori, nama_file):
    if data:
        df = pd.DataFrame(data)
        file_path = os.path.join(direktori, nama_file)
        df.to_csv(file_path, index=False)
        print(f"Data berhasil disimpan ke: {file_path}")
    else:
        print("Tidak ada data untuk disimpan.")

# Main program
if __name__ == "__main__":
    nama_direktori = "data_sinta"
    buat_direktori(nama_direktori)
    
    # Ambil data dari halaman pertama
    print("Mengambil data dari Sinta...")
    data_kampus = scrape_sinta(page=1)
    
    # Simpan data ke CSV
    nama_file = "data_kampus_sinta.csv"
    simpan_data_ke_csv(data_kampus, nama_direktori, nama_file)
