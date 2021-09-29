import requests
from bs4 import BeautifulSoup

numberOfAnimeToScrape = 100
urlArray = []
data = []

for x in range(int(numberOfAnimeToScrape/50)):
  urlArray.append(f'https://myanimelist.net/topanime.php?limit={x*50}')  

def getTitlesAndScores(url, data):
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  animeList = soup.find_all('tr', class_='ranking-list')
  for anime in animeList:
    title = anime.find('td', class_='title').select('a')[1].text
    score = anime.find('td', class_='score').select('span')[0].text
    data.append({'title': title, 'score': score})

  print(len(data))

for url in urlArray:
  getTitlesAndScores(url, data)

file = open('anime.csv', 'w')
file.write('Title, Score \n')
for anime in data:
  file.write(f"{anime['title']}, {anime['score']} \n")

file.close()