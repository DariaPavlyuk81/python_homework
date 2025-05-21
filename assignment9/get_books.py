# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By


# #Task1

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# robots_url = "https://durhamcountylibrary.org/robots.txt"
# driver.get(robots_url)
# print(driver.page_source)
# driver.quit()


#Task3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import time

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


# Load the webpage
url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
driver.get(url)

time.sleep(5)


#  <li> elements 
list_items = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
print(f"Found {len(list_items)} search result items.")

results = []

for li in list_items:
    try:
        #  the title
        title_el = li.find_element(By.CSS_SELECTOR, "h2.cp-title")
        title = title_el.text.strip() if title_el else "Unknown"
        

        #  authors (may have more than one)
        author_elements = li.find_elements(By.CSS_SELECTOR, "a.author-link")
        authors = "; ".join([a.text.strip() for a in author_elements if a.text.strip()]) or "Unknown"

        #  format and year info
        format_year_elements = li.find_elements(By.CSS_SELECTOR, "div.manifestation-item-format-call-wrap.available span.display-info-primary")
        format_year = format_year_elements[0].text.strip() if format_year_elements else "Unknown"

        # dictionary
        book_data = {
            "Title": title,
            "Author": authors,
            "Format-Year": format_year
        }

        results.append(book_data)

    except Exception as e:
        
        print(f"Skipped one item due to error: {e}")


driver.quit()


df = pd.DataFrame(results)
print(df)



#Task4 write out the data
# Save as JSON or CSV
# df.to_json("books.json", indent=2)


# df.to_csv("books.csv", index=False)

#Task5 Ethical web scraping


   
    