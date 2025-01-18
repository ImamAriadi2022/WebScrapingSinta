from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from helper import save_to_csv
import logging
import os
import time

# Konfigurasi logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/scraping.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# URL target
BASE_URL = "https://sinta.kemdikbud.go.id/affiliations/profile/384"

def scrape_data():
    """Fungsi utama untuk melakukan scraping menggunakan Selenium."""
    # Konfigurasi Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Untuk menjalankan browser tanpa GUI
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    service = Service(executable_path="drivers/chromedriver.exe")  # Pastikan 'chromedriver.exe' berada di path yang benar
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        logging.info("Memulai scraping data dari halaman.")
        driver.get(BASE_URL)
        time.sleep(5)  # Tunggu beberapa saat agar JavaScript selesai dimuat

        # Simpan halaman setelah dimuat untuk debugging
        with open("logs/page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Parsing dengan BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.select("tr")  # Selektor tabel
        
        if not rows:
            logging.warning("Tidak menemukan elemen tabel di halaman.")
        else:
            logging.info(f"Ditemukan {len(rows)-1} baris data dalam tabel.")
        
        # Proses data tabel
        kampus_list = []
        for idx, row in enumerate(rows[1:], start=1):  # Skip header tabel
            cols = row.find_all("td")
            if len(cols) >= 2:
                nama_kampus = cols[1].get_text(strip=True)
                alamat = cols[2].get_text(strip=True) if len(cols) > 2 else "-"
                # Filter kampus yang memiliki departemen/prodi komputer
                if any(prodi in nama_kampus for prodi in ["SI", "TI", "SK", "MTI", "Sains Data"]):
                    kampus_list.append([idx, nama_kampus, alamat])
                    print(f"Data ditemukan: {idx}, {nama_kampus}, {alamat}")  # Debugging

        # Simpan data ke file CSV
        if kampus_list:
            save_to_csv(kampus_list, "../data/data_kampus.csv")
            logging.info(f"Data berhasil disimpan di ../data/data_kampus.csv")
        else:
            logging.warning("Tidak ada data kampus yang disimpan karena kosong.")
    except Exception as e:
        logging.exception(f"Terjadi kesalahan: {e}")
    finally:
        driver.quit()  # Tutup browser

if __name__ == "__main__":
    scrape_data()