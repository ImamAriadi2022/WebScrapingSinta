from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import os
import time
from helpersainsdata import save_to_csv  # Impor fungsi save_to_csv dari helpersainsdata

# Konfigurasi logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/scraping_sainsdata.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# URL target
BASE_URL = "https://edukasi.sindonews.com/read/1352303/211/mau-kuliah-prodi-sains-data-daftar-saja-di-7-ptn-unggulan-ini-1712030671"

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
        time.sleep(5)  # Tunggu beberapa saat agar halaman selesai dimuat

        # Ambil semua elemen h3
        h3_elements = driver.find_elements(By.TAG_NAME, "h3")
        h3_texts = [element.text for element in h3_elements if element.text.strip()]

        # Simpan data ke file CSV
        if h3_texts:
            save_to_csv(h3_texts, "data/daftar_ptn_sainsdata.csv")
            logging.info(f"Data berhasil disimpan di data/daftar_ptn_sainsdata.csv")
        else:
            logging.warning("Tidak ada data h3 yang disimpan karena kosong.")
    except Exception as e:
        logging.exception(f"Terjadi kesalahan: {e}")
    finally:
        driver.quit()  # Tutup browser

if __name__ == "__main__":
    scrape_data()