import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.parse import urljoin

# MongoDB connection - 
client = MongoClient('mongodb+srv://kirtanchandak:si6cnFfs5CKEUbr1@cornellblog.4c5hnap.mongodb.net/?retryWrites=true&w=majority')
db = client['auditLinks']
collection = db['links']

url = "https://code4rena.com/reports/2023-01-blockswap-fv/"

# get html
r = requests.get(url)
htmlContent = r.content

# parse the html 
soup = BeautifulSoup(htmlContent, 'html.parser')

# html tree traversal
div = soup.find('div', class_='report-toc')
div_text = div.text
links = div.find_all('a') 

name = soup.find('div', class_='report-header')
name_text = name.find('h1')

for name in name_text:
    name = name_text.contents[0].strip()

link_data = [] 

for link in links:
    link_text = link.text
    link_href = link.get('href')
    if link_href:
        full_link = urljoin(url, link_href)
        link_data.append({'text': link_text, 'href': full_link})

data = {
    "links": link_data,
    "name": name
}

collection.insert_one(data)

client.close()