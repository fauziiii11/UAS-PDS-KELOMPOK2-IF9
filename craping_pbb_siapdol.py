from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


# SETUP BROWSER
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(
    service=service,
    options=options
)



# BUKA HALAMAN SIAPDOL
url = "https://siapdol.sumedangkab.go.id/siapdol/pbb/realisasi_desa/buku123/030"
driver.get(url)


time.sleep(60)  


# TUNGGU TABEL MUNCUL
wait = WebDriverWait(driver, 60)
table = wait.until(
    EC.presence_of_element_located((By.TAG_NAME, "table"))
)

rows = table.find_elements(By.TAG_NAME, "tr")

data = []

for row in rows[1:]:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 4:
        data.append({
            "Jalan OP": cols[0].text.strip(),
            "Nama WP": cols[1].text.strip(),
            "NOP": cols[2].text.strip(),
            "PBB": cols[3].text.strip()
        })

driver.quit()


# DATAFRAME & CLEANING
df = pd.DataFrame(data)

df["PBB"] = (
    df["PBB"]
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .astype(float)
)

# SIMPAN KE EXCEL
output = "Data_pbb_siapdol.xlsx"
df.to_excel(output, index=False)

print(f"✅ Scraping selesai. Data tersimpan: {output}")
