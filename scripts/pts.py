import requests
from bs4 import BeautifulSoup
import csv

# URL target
URL = "https://id.wikipedia.org/wiki/Daftar_perguruan_tinggi_swasta_di_Indonesia"

def scrape_data():
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    data_list = []

    # Cari semua elemen <a> yang mengandung link ke provinsi
    province_links = soup.find_all("a", href=True, title=True)
    for link in province_links:
        if "/wiki/" in link['href'] and link['href'].startswith("/wiki/") and link['title'] != "Indonesia":
            province_name = link.get_text(strip=True)
            province_url = f"https://id.wikipedia.org{link['href']}"
            print(f"Scraping data for province: {province_name}")

            # Request halaman provinsi
            province_response = requests.get(province_url)
            if province_response.status_code != 200:
                print(f"Failed to retrieve the province page. Status code: {province_response.status_code}")
                continue

            province_soup = BeautifulSoup(province_response.content, "html.parser")
            # Cari semua elemen <td> yang mengandung link ke universitas
            university_cells = province_soup.find_all("td", width="30%")
            for cell in university_cells:
                university_link = cell.find("a", href=True, title=True)
                if university_link:
                    university_name = university_link.get_text(strip=True)
                    data_list.append([province_name, university_name])
                    print(f"Found university: {university_name} in {province_name}")

    # Simpan data ke file CSV
    with open("data/daftar_pts.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Province", "University"])
        writer.writerows(data_list)
        print("Data has been saved to data/daftar_pts.csv")

if __name__ == "__main__":
    scrape_data()