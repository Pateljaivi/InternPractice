# import requests
#
# from bs4 import BeautifulSoup
#
# url = "https://www.flipkart.com"
# r = requests.get(url)
# r.encoding = "utf-8"
# print(r.status_code)

# import requests
# from bs4 import BeautifulSoup
#
#
# def fetch_page(url):
#     headers = {
#         "User-Agent": "Mozilla/5.0",
#         "Accept-Language": "en-US,en;q=0.9"
#     }
#     response = requests.get(url, headers=headers)
#     return response.text
#
#
# def extract_products(html):
#     soup = BeautifulSoup(html, "html.parser")
#     products = []
#
#     items = soup.find_all("div", class_="_1AtVbE")
#
#     for item in items:
#         name = item.find("div", class_="_4rR01T")
#         price = item.find("div", class_="_30jeq3 _1_WHN1")
#         rating = item.find("div", class_="_3LWZlK")
#
#         if name and price:
#             products.append({
#                 "Name": name.text,
#                 "Price": price.text,
#                 "Rating": rating.text if rating else "No Rating"
#             })
#
#     return products
#
#
# def main():
#     url = "https://www.flipkart.com/search?q=iphone"
#
#     html = fetch_page(url)
#     products = extract_products(html)
#
#     print("\n--- Flipkart Products ---\n")
#     for p in products[:5]:  # Only first 5 products
#         print("Name:", p["Name"])
#         print("Price:", p["Price"])
#         print("Rating:", p["Rating"])
#         print("-" * 40)
#
#
# if __name__ == "__main__":
#     main()

import requests
from bs4 import BeautifulSoup


# -----------------------------
# 1. Fetch HTML
# -----------------------------
def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    return response.text


# -----------------------------
# 2. Extract Title
# -----------------------------
def extract_title(soup):
    title = soup.find("h1")
    return title.get_text(strip=True) if title else "No Title Found"


# -----------------------------
# 3. Extract Headings & Paragraphs
# -----------------------------
def extract_content(soup):
    content_data = []

    for tag in soup.find_all(["h2", "h3", "p"]):
        text = tag.get_text(strip=True)
        if text:
            content_data.append(text)

    return content_data


# -----------------------------
# 4. Extract Code Blocks
# -----------------------------
def extract_code(soup):
    codes = []
    for code in soup.find_all("pre"):
        codes.append(code.get_text())
    return codes


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def main():
    url = "https://www.geeksforgeeks.org/web-scraping/introduction-to-web-scraping/"

    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    print("\n--- TITLE ---\n")
    print(extract_title(soup))

    print("\n--- CONTENT ---\n")
    content = extract_content(soup)
    for line in content[:20]:  # limit output
        print(line)

    print("\n--- CODE SNIPPETS ---\n")
    codes = extract_code(soup)
    for c in codes:
        print(c)
        print("-" * 50)


if __name__ == "__main__":
    main()