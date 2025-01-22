from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import os
import time
from helperdatalengkap import save_to_csv  # Impor fungsi save_to_csv dari helperdatalengkap

# Konfigurasi logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/scraping_datalengkap.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# URL target
BASE_URL = "https://sinta.kemdikbud.go.id/affiliations"

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

        data_list = []
        current_page = 1

        while True:
            logging.info(f"Sedang di halaman {current_page}")
            # Ambil semua elemen dengan class "list-item row mb-4"
            list_items = driver.find_elements(By.CLASS_NAME, "list-item.row.mb-4")
            for index in range(len(list_items)):
                # Ambil ulang semua elemen dengan class "list-item row mb-4" setelah kembali ke halaman utama
                list_items = driver.find_elements(By.CLASS_NAME, "list-item.row.mb-4")
                item = list_items[index]

                # Cari elemen <a> di dalam item dan klik
                link = item.find_element(By.TAG_NAME, "a")
                university_name = link.text.strip()
                link.click()
                time.sleep(5)  # Tunggu beberapa saat agar halaman selesai dimuat

                # Cari elemen <tr> yang berisi data
                try:
                    tr_element = driver.find_element(By.XPATH, "//tr[td[text()='Documents']]")
                    scopus_value = tr_element.find_element(By.CLASS_NAME, "text-warning").text.strip()
                    gscholar_value = tr_element.find_element(By.CLASS_NAME, "text-success").text.strip()
                    garuda_value = tr_element.find_element(By.CLASS_NAME, "text-danger").text.strip()
                    data_list.append([university_name, scopus_value, gscholar_value, garuda_value])
                    logging.info(f"Data ditemukan: {university_name}, Scopus: {scopus_value}, GScholar: {gscholar_value}, Garuda: {garuda_value}")
                except Exception as e:
                    logging.warning(f"Data tidak ditemukan untuk {university_name}: {e}")

                # Kembali ke halaman utama
                driver.get(f"{BASE_URL}?page={current_page}")
                time.sleep(5)  # Tunggu beberapa saat agar halaman selesai dimuat

            # Cek apakah ada tombol "Next"
            try:
                next_button = driver.find_element(By.XPATH, "//a[contains(@class, 'page-link') and contains(text(), 'Next')]")
                next_button.click()
                current_page += 1
                time.sleep(5)  # Tunggu beberapa saat agar halaman berikutnya dimuat
            except Exception as e:
                logging.info("Tidak ada tombol 'Next' atau tombol tidak dapat diklik.")
                break

        # Simpan data ke file CSV
        if data_list:
            save_to_csv(data_list, "data/daftar_kampus_datalengkap.csv")
            logging.info(f"Data berhasil disimpan di data/daftar_kampus_datalengkap.csv")
        else:
            logging.warning("Tidak ada data yang disimpan karena kosong.")
    except Exception as e:
        logging.exception(f"Terjadi kesalahan: {e}")
    finally:
        driver.quit()  # Tutup browser

if __name__ == "__main__":
    scrape_data()