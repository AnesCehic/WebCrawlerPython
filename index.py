from bs4 import BeautifulSoup
import requests
import csv

base_url = "https://get.todoist.help"
url = requests.get(base_url + "/hc/en-us/categories/115000626249")

data = url.text
soup = BeautifulSoup(data)

faq = soup.find_all("section", attrs={'class': 'dth-section'})

links_and_sections = {}

for links in faq:
  link = links.h2.a['href']
  key = links.h2.a.text.strip()

  links_and_sections[key] = []
  
  url_by_tag = requests.get(base_url + link)
  data = url_by_tag.text
  
  lists = BeautifulSoup(data)
  li = lists.find_all("li", attrs={"class": "dth-articles__item"})

  for li2 in li:
  
    links_and_sections[key].append((li2.a["href"], li2.a.text))


print(links_and_sections)

for key in links_and_sections:
  with open(key + '.csv', 'w') as out:
    file = csv.writer(out)
    file.writerow(['link', 'heading'])

    for row in links_and_sections[key]:
      file.writerow([row[0], row[1]])

print("Done")