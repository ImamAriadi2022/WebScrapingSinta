from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import logging
import os
import time
from helpermti import save_to_csv  # Impor fungsi save_to_csv dari helpermti

# Konfigurasi logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/scraping_mti.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# URL target
BASE_URL = "file:///c:/Users/asus/Downloads/WebScrapingSinta/scripts/mti.html"

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

        kampus_list = []

        while True:
            # Parsing dengan BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Cari elemen dengan class "schools-found"
            schools_found = soup.find("div", class_="schools-found")
            if schools_found:
                logging.info(schools_found.get_text(strip=True))
            else:
                logging.warning("Elemen 'schools-found' tidak ditemukan.")
                break

            # Ambil semua elemen kampus
            kampus_elements = soup.find_all("div", class_="m-y-sm col-xs-12 col col-sm-6 col-md-4")
            for kampus_element in kampus_elements:
                nama_kampus_element = kampus_element.find("h4", class_="campus-perfect-card__title")
                if nama_kampus_element:
                    nama_kampus = nama_kampus_element.get_text(strip=True)
                    kampus_list.append([nama_kampus, "Manajemen Informatika"])
                    logging.info(f"Data ditemukan: {nama_kampus}")

            # Cek apakah ada tombol "Lihat kampus lain" di dalam "school-card-list-container"
            try:
                school_card_list_container = driver.find_element(By.CLASS_NAME, "school-card-list-container")
                see_more_button = school_card_list_container.find_element(By.CLASS_NAME, "see-more-schools")
                driver.execute_script("arguments[0].scrollIntoView(true);", see_more_button)
                time.sleep(1)  # Tunggu sebentar setelah scroll
                see_more_button.click()
                time.sleep(5)  # Tunggu beberapa saat agar halaman berikutnya dimuat
            except Exception as e:
                logging.info("Tidak ada tombol 'Lihat kampus lain' atau tombol tidak dapat diklik.")
                break

        # Simpan data ke file CSV
        if kampus_list:
            save_to_csv(kampus_list, "data/daftar_kampus_mti.csv")
            logging.info(f"Data berhasil disimpan di data/daftar_kampus_mti.csv")
        else:
            logging.warning("Tidak ada data kampus yang disimpan karena kosong.")
    except Exception as e:
        logging.exception(f"Terjadi kesalahan: {e}")
    finally:
        driver.quit()  # Tutup browser

if __name__ == "__main__":
    scrape_data()