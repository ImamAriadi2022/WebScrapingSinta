import requests
from bs4 import BeautifulSoup
import pandas as pd

# Contoh scraping dari Sinta (sesuaikan URL dan struktur HTML)
url = "https://sinta.kemdikbud.go.id/affiliations"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Ambil data kampus
kampus_list = []
for row in soup.find_all('tr')[1:]:  # Skip header
    columns = row.find_all('td')
    if len(columns) > 2:
        kampus = columns[1].text.strip()  # Nama kampus
        score = columns[2].text.strip()  # Sinta Score
        kampus_list.append({"Kampus": kampus, "Sinta Score": score})

# Convert ke DataFrame dan simpan ke CSV
df = pd.DataFrame(kampus_list)
df.to_csv("data_kampus.csv", index=False)
print("Data berhasil disimpan!")
