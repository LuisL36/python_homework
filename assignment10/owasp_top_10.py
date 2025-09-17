from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://owasp.org/Top10/"
driver.get(url)

wait = WebDriverWait(driver, 10)
vulnerability_elements = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//a[starts-with(@href,'https://owasp.org/Top10/A') and contains(@href,'2021')]")
    )
)

vulnerabilities = []
for elem in vulnerability_elements:
    title = elem.text.strip()
    if title:  # skip empty links
        link = elem.get_attribute("href")
        vulnerabilities.append({"Title": title, "Link": link})

df = pd.DataFrame(vulnerabilities)
df.to_csv("owasp_top_10.csv", index=False)

print(df)
driver.quit()
