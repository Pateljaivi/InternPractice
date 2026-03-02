import requests
from bs4 import BeautifulSoup

with open("sample.html","r") as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc,"html.parser")
# print(soup.prettify())
# print(soup.title,type(soup.title))
# print(soup.div)

# print(soup.find_all("div")[0])

# for link in soup.find_all('a'):
#     print(link.get('href'))
#     print(link.get_text())
#
# s = soup.find(id = "link3")
# print(s.get("href"))

# print(soup.select("div.italic"))
# print(soup.select("span#italic"))

# print(soup.find(class_="italic"))
# print(soup.find_all(class_="italic"))

# for child in soup.find(class_ = "container").children:
#     print(child)

# for parent in soup.find(class_ = "box").parents:
#     print(parent)

# cont = soup.find(class_="container")
# cont.name = "jaivi"
# print(cont)

# ulTag = soup.new_tag("ul")
#
# liTag = soup.new_tag("li")
# liTag.string = "Home"
# ulTag.append(liTag)
#
# liTag = soup.new_tag("li")
# liTag.string = "About"
# ulTag.append(liTag)
#
# soup.html.body.insert(0,ulTag)
#
# with open("sample.html","w") as f:
#     f.write(str(soup))

cont = soup.find(class_="container")
print(cont.has_attr("class"))