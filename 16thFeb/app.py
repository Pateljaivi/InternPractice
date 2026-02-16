from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from datetime import datetime


BASE_URL = "https://www.scrapethissite.com/pages/forms/"
CSV_FILENAME = "nhl_teams_selenium_all.csv"

HEADLESS = True
PAGE_DELAY = 1.8  # polite delay between pages

def init_driver():
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) EducationalSelenium/1.0")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=chrome_options)
    return driver

def scrape_page(driver,wait:WebDriverWait,page_num:int)->list[dict]:
    url = f"{BASE_URL}?page_num={page_num}"
    print(f"Loading:{url}")
    driver.get(url)

    teams = []

    try:
        wait.untill(EC.presence_of_element_located((By.CSS_SELECTOR,"tr.team")))

        team_rows = driver.find_elements(By.CSS_SELECTOR,"tr.team")
        print(f" Page {page_num}: Found {len(team_rows)} teams")

        for row in team_rows:
            try:
                team = {
                    "Team" : row.find_element(By.CSS_SELECTOR,"td.name").text.strip(),
                    "Year" : row.find_element(By.CSS_SELECTOR,"td.year").text.strip(),
                    "Wins" : row.find_element(By.CSS_SELECTOR,"td.wins").text.strip(),
                    "Losses": row.find_element(By.CSS_SELECTOR,"td.losses").text.strip(),
                    "OTL": row.find_element(By.CSS_SELECTOR,"td.ot-losses").text.strip() or "",
                    "Win%": row.find_element(By.CSS_SELECTOR,"td.win%").text.strip(),
                    "GF" : row.find_element(By.CSS_SELECTOR,"td.gf").text.strip(),
                    "GA" : row.find_element(By.CSS_SELECTOR,"td.ga").text.strip(),
                    "+/-": row.find_element(By.CSS_SELECTOR,"td.diff").text.strip(),
                }
                teams.append(team)
            except:
                continue
    except Exception as e:
                print(f"Page {page_num} extraction failed:{e}")

    return teams

