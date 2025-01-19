from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from helperdaftar import save_to_csv
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
BASE_URL = "https://id.wikipedia.org/wiki/Daftar_perguruan_tinggi_negeri_di_Indonesia"

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
        logging.info("Memulai scraping data dari halaman utama.")
        driver.get(BASE_URL)
        time.sleep(5)  # Tunggu beberapa saat agar JavaScript selesai dimuat

        # Simpan halaman setelah dimuat untuk debugging
        with open("logs/daftarkampus.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Parsing dengan BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Ambil semua elemen tr
        rows = soup.find_all('tr')
        logging.info(f"Ditemukan {len(rows)} elemen tr.")
        
        kampus_list = []
        
        for row in rows:
            cols = row.find_all('td', style="text-align:left;")
            if len(cols) >= 2:
                nama_kampus_element = cols[0].find('a', title=True)
                lokasi_kampus_element = cols[1].find('a', title=True)
                
                if nama_kampus_element and lokasi_kampus_element:
                    nama_kampus = nama_kampus_element.get_text(strip=True)
                    lokasi_kampus = lokasi_kampus_element.get_text(strip=True)
                    kampus_list.append([nama_kampus, lokasi_kampus])
                    logging.info(f"Data ditemukan: {nama_kampus}, {lokasi_kampus}")

        # Simpan data ke file CSV
        if kampus_list:
            save_to_csv(kampus_list)
            logging.info(f"Data berhasil disimpan di data/daftar_kampus_indo.csv")
        else:
            logging.warning("Tidak ada data kampus yang disimpan karena kosong.")
    except Exception as e:
        logging.exception(f"Terjadi kesalahan: {e}")
    finally:
        driver.quit()  # Tutup browser

if __name__ == "__main__":
    scrape_data()