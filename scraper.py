import requests
import re
from bs4 import BeautifulSoup

numberOfAnimeToScrape = 50
urlArray = []
data = []

for x in range(int(numberOfAnimeToScrape/50)):
  urlArray.append(f'https://myanimelist.net/topanime.php?limit={x*50}')  

def getTitlesAndScores(url, data):
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  animeList = soup.find_all('tr', class_='ranking-list')
  # the code below is slowing down the scraper significantly (likely due to the http requests being made within the for loop)
  for anime in animeList:
    title = anime.find('td', class_='title').select('a')[1].text
    score = anime.find('td', class_='score').select('span')[0].text
    detailsURL = anime.find('td', class_='title').select('a')[1]['href']
    detailsPage = requests.get(detailsURL)
    detailsSoup = BeautifulSoup(detailsPage.content, 'html.parser')
    prequel = detailsSoup.find(text=re.compile("Prequel:")) == "Prequel:"
    data.append({'title': title, 'score': score, 'prequel': prequel})

  print(len(data))

for url in urlArray:
  getTitlesAndScores(url, data)

file = open('anime.csv', 'w')
file.write('Title, Score, Prequel Exists \n')
for anime in data:
  file.write(f"{anime['title']}, {anime['score']}, {anime['prequel']} \n")

file.close()

# https://codereview.stackexchange.com/questions/155681/optimizing-the-speed-of-a-web-scraper
# Going to use the above page to start optimising the scraper cause it's slow as hell the way it is now