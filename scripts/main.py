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
BASE_URL = "https://sinta.kemdikbud.go.id/affiliations?page="

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
        
        kampus_list = []
        page = 1
        
        while True:
            current_url = BASE_URL + str(page)
            logging.info(f"Mengambil data dari {current_url}")
            
            # Tambahkan retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    driver.set_page_load_timeout(180)  # Tingkatkan timeout menjadi 180 detik
                    driver.get(current_url)
                    break
                except Exception as e:
                    logging.warning(f"Percobaan {attempt + 1} gagal: {e}")
                    if attempt == max_retries - 1:
                        raise

            time.sleep(5)  # Tunggu beberapa saat agar JavaScript selesai dimuat

            # Simpan halaman setelah dimuat untuk debugging
            with open(f"logs/page_source_{page}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

            # Parsing dengan BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Ambil semua elemen a untuk nama kampus
            kampus_elements = soup.find_all('a', href=True)
            print(f"Ditemukan {len(kampus_elements)} elemen a dengan href.")  # Debugging
            
            # Filter elemen a dengan class 'affil-name'
            kampus_elements = [a for a in kampus_elements if 'affiliations/profile' in a['href']]
            print(f"Ditemukan {len(kampus_elements)} elemen a dengan href yang mengandung 'affiliations/profile'.")  # Debugging
            
            # Ambil semua elemen div dengan class 'pr-num' untuk Sinta score
            sinta_elements = soup.find_all('div', class_='pr-num')
            print(f"Ditemukan {len(sinta_elements)} elemen div pr-num.")  # Debugging
            
            if not kampus_elements or not sinta_elements:
                logging.warning("Tidak menemukan elemen kampus atau Sinta score di halaman.")
                break
            else:
                logging.info(f"Ditemukan {len(kampus_elements)} kampus dan {len(sinta_elements)} Sinta score.")
            
            # Proses data kampus dan Sinta score
            for i in range(len(kampus_elements)):
                nama_kampus = kampus_elements[i].get_text(strip=True)
                sinta_score = sinta_elements[i * 2].get_text(strip=True)  # Ambil hanya elemen pr-num pertama
                kampus_list.append([nama_kampus, sinta_score])
                print(f"Data ditemukan: {nama_kampus}, {sinta_score}")  # Debugging

            # Cek apakah ada halaman berikutnya
            next_button = soup.find('a', class_='page-link', text='Next')
            if next_button:
                page += 1
            else:
                break

        # Simpan data ke file CSV
        if kampus_list:
            save_to_csv(kampus_list, "data/data_kampus.csv")
            logging.info(f"Data berhasil disimpan di ../data/data_kampus.csv")
        else:
            logging.warning("Tidak ada data kampus yang disimpan karena kosong.")
    except Exception as e:
        logging.exception(f"Terjadi kesalahan: {e}")
    finally:
        driver.quit()  # Tutup browser

if __name__ == "__main__":
    scrape_data()