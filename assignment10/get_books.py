from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
driver.get(url)

wait = WebDriverWait(driver, 15)
results_list = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cp-search-result-item")))

results = []

for item in results_list:
    try:
        title = item.find_element(By.CLASS_NAME, "cp-title").text.strip()
    except:
        title = ""

    try:
        author_links = item.find_elements(By.CSS_SELECTOR, "a.author-link")
        authors = "; ".join([a.text.strip() for a in author_links if a.text.strip()])
    except:
        authors = ""

    try:
        display_info = item.find_element(By.CSS_SELECTOR, "span.display-info-primary").text.strip()
        format_year = display_info
    except:
        format_year = ""

    if title:
        results.append({
            "Title": title,
            "Author": authors,
            "Format-Year": format_year
        })

df = pd.DataFrame(results)
df.to_csv("get_books.csv", index=False)
with open("get_books.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(df.head(10))
driver.quit()
