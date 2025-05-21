from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

url = "https://owasp.org/www-project-top-ten/"
driver.get(url)
time.sleep(5)


vulnerabilities = []
items = driver.find_elements(By.XPATH, "/html/body/main/div/div[1]/section[1]/ul[2]/li/a")

for item in items[:10]:  
    title = item.text.strip()
    href = item.get_attribute("href")
    vulnerabilities.append({
        "Title": title,
        "Link": href
    })

driver.quit()

# Print to verify
for vuln in vulnerabilities:
    print(vuln)

# Save to CSV
df = pd.DataFrame(vulnerabilities)
df.to_csv("owasp_top_10.csv", index=False)