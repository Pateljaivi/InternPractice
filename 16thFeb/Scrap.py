# import requests
# from bs4 import BeautifulSoup
#
# url = "https://www.w3schools.com/html/html_tables.asp"
#
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")
#
# # find the specific table
# table = soup.find("table",{"id":"customers"})
#
# rows = table.find_all("tr")
#
# for i,row in enumerate(rows):
#     cells = row.find_all(["th","td"])
#     cell_text = [cell.text.strip() for cell in cells]
#     print(cell_text)
#
# #find all headings
# headings = soup.find_all(["h1","h2"])
# print("Headings from the page:\n")
#
# for heading in headings:
#     print(heading.get_text().strip())
#
#
# #find all anchor tags
#
# links = soup.find_all("a")
#
# print("All links from the page.\n")
#
# for link in links:
#     link_text = link.get_text().strip()
#     link_href = link.get("href")
#
#     if link_href:
#         print("Text:",link_text)
#         print("URL:",link_href)
#         print("-"*40)


import requests
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime

BASE_URL = "https://www.scrapethissite.com/pages/forms/"

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64; x64) EducationalScraper/1.0'
           }

DELAY_BETWEEN_PAGES = 2.0
CSV_FILENAME = "nhl_teams_all.csv"


def get_teams_from_page(page_num: int) -> list[dict]:
    """Fetch and parse one page of teams"""
    url = f"{BASE_URL}?page_num={page_num}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Select all rows with class="team"
        team_rows = soup.select("tr.team")

        if not team_rows:
            print(f"  Page {page_num}: No team rows found → probably end of data")
            return []

        teams = []

        for row in team_rows:
            name_cell = row.select_one("td.name")
            year_cell = row.select_one("td.year")
            wins_cell = row.select_one("td.wins")
            losses_cell = row.select_one("td.losses")
            otl_cell = row.select_one("td.ot-losses")
            pct_cell = row.select_one("td.pct")
            gf_cell = row.select_one("td.gf")
            ga_cell = row.select_one("td.ga")
            diff_cell = row.select_one("td.diff")

            if not name_cell or not year_cell:
                continue

            team = {
                "Team": name_cell.get_text(strip=True),
                "Year": year_cell.get_text(strip=True),
                "Wins": wins_cell.get_text(strip=True) if wins_cell else "",
                "Losses": losses_cell.get_text(strip=True) if losses_cell else "",
                "OTL": otl_cell.get_text(strip=True) if otl_cell else "",
                "Win%": pct_cell.get_text(strip=True) if pct_cell else "",
                "GF": gf_cell.get_text(strip=True) if gf_cell else "",
                "GA": ga_cell.get_text(strip=True) if ga_cell else "",
                "+/-": diff_cell.get_text(strip=True) if diff_cell else ""
            }
            teams.append(team)

        print(f"  Page {page_num}: scraped {len(teams)} teams")
        return teams

    except requests.RequestException as e:
        print(f"  Page {page_num}: Request failed → {e}")
        return []
    except Exception as e:
        print(f"  Page {page_num}: Parsing error → {e}")
        return []


def scrape_all_pages():
    """Loop through pages until no more data"""
    all_teams = []
    page = 1

    while True:
        print(f"\nScraping page {page}...")
        page_teams = get_teams_from_page(page)

        if not page_teams:
            print("  → No more teams found. Stopping.")
            break

        all_teams.extend(page_teams)
        page += 1

        # Be polite - don't hammer the server
        if page_teams:  # only delay if we got data
            time.sleep(DELAY_BETWEEN_PAGES)

    return all_teams


def save_to_csv(teams: list[dict]):
    """Export scraped data to CSV"""
    if not teams:
        print("No data to save.")
        return

    # Use first team's keys as headers
    fieldnames = teams[0].keys()

    with open(CSV_FILENAME, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(teams)

    print(f"\nSaved {len(teams)} teams to {CSV_FILENAME}")


if __name__ == "__main__":
    print("=== NHL Teams Full Scraper with Pagination & CSV ===")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    start_time = time.time()

    all_nhl_teams = scrape_all_pages()

    print(f"\nTotal teams scraped: {len(all_nhl_teams)}")

    save_to_csv(all_nhl_teams)

    elapsed = time.time() - start_time
    print(f"\nFinished in {elapsed:.2f} seconds ({elapsed / 60:.1f} minutes)")