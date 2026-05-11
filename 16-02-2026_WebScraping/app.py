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

HEADLESS = False#headless ek boolean var hai if it is True = browser background me chalega if false=browser screen pe dikhega
PAGE_DELAY = 1.8  # polite delay between pages->server ko overload na kare

def init_driver(): #this function will start browser
    chrome_options = Options() #crome setting object bana raha hai
    if HEADLESS: #if hadless true hai to
        chrome_options.add_argument("--headless=new")  #browser invisible mode me chalega means bachground me  chalega
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        #ye sab server pe error avoid karne ke liye best practice options hain

    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) EducationalSelenium/1.0")
    #website ko batata hain ki hum normal browser hain(bot nahi)

    service = Service(ChromeDriverManager().install()) #automatically chromedriver download and setup karega
    driver = webdriver.Chrome(service=service,options=chrome_options)#chrome browser start kar diya
    return driver#driver wapas bhej diya



#this function page scrape karega,take page num and return dictionary list
def scrape_page(driver,wait:WebDriverWait,page_num:int)->list[dict]:
    url = f"{BASE_URL}?page_num={page_num}"#direct url pagination use kar rahe hain
    print(f"Loading:{url}")
    driver.get(url) #browser us page pe chala gaya

    teams = []

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"tr.team")))#wait karega jab tak table rows load na ho jaye

        team_rows = driver.find_elements(By.CSS_SELECTOR,"tr.team") #share team rows find kar liye
        print(f" Page {page_num}: Found {len(team_rows)} teams")

        for row in team_rows:
            try:
                team = {
                    "Team" : row.find_element(By.CSS_SELECTOR,"td.name").text.strip(),#row ke under team name nikala,text value nikala,strip ke through extra space hata diya
                    "Year" : row.find_element(By.CSS_SELECTOR,"td.year").text.strip(),
                    "Wins" : row.find_element(By.CSS_SELECTOR,"td.wins").text.strip(),
                    "Losses": row.find_element(By.CSS_SELECTOR,"td.losses").text.strip(),
                    "OTL": row.find_element(By.CSS_SELECTOR,"td.ot-losses").text.strip() or "",
                    "Win%": row.find_element(By.CSS_SELECTOR,"td.pct").text.strip(),
                    "GF" : row.find_element(By.CSS_SELECTOR,"td.gf").text.strip(),
                    "GA" : row.find_element(By.CSS_SELECTOR,"td.ga").text.strip(),
                    "+/-": row.find_element(By.CSS_SELECTOR,"td.diff").text.strip(),
                }
                teams.append(team) #store all into dict
            except:
                continue
    except Exception as e:
                print(f"Page {page_num} extraction failed:{e}")

    return teams


#scrape all pages function->pura website scrape karega
def scrape_all_pages():
    driver = init_driver()#browser start
    all_teams = []
    page_num = 1#page 1 se start

    wait = WebDriverWait(driver, 12)

    try:
        while True:
            page_teams = scrape_page(driver,wait,page_num)#current page scrap kiya call the function

            if not page_teams: #if data not found means last page->loop stop
                print(f" Page{page_num}:No teams -> stopping")
                break

            all_teams.extend(page_teams)#current page ka data main list me add
            page_num += 1 #next page
            time.sleep(PAGE_DELAY) #for some delay between pages

    finally:
        driver.quit()#browser close
        print("Browser closed.")

    return all_teams


#save to csv function
def save_to_csv(teams: list[dict]):
    if not teams:
        print("No data scraped.")
        return

    fieldnames = teams[0].keys()#dictionary ke keys ko header bana diya

    with open(CSV_FILENAME, "w", newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)#CSv writer object banaya
        writer.writeheader()#header likha
        writer.writerows(teams)#sare rows file me likh diye

    print(f"saved {len(teams)} teams to {CSV_FILENAME}")



if __name__ == "__main__":
    print("=== Selenium Demo - NHL Teams (URL Pagination) ===")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    start_time = time.time()

    teams_data = scrape_all_pages()#pura scraping run hoga

    print(f"\nTotal teams:{len(teams_data)}")
    save_to_csv(teams_data)

    elapsed = time.time() - start_time #total time calculate hoga
    print(f"\nFinished in {elapsed:.2f} seconds (~{elapsed/60:.1f} min)")

    print("\nTeaching points:")
    print("  • Prefer URL-based pagination when available → simpler & more reliable")
    print("  • Avoid clicking if possible — reduces flakiness")
    print("  • Use driver.get() to jump directly to any page")
    print("  • This site doesn't need Selenium, but shows how to handle dynamic cases")
