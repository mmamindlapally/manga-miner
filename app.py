import requests
import tempfile
from bs4 import BeautifulSoup

URL = "http://www.mangareader.net"

search_string = input("Enter your Manga: ")
search_string.replace(" ", "+")

page = requests.get(URL + "/search/?w=" + search_string)
soup = BeautifulSoup(page.content, 'html.parser')

mangaresults = soup.find(id = 'mangaresults')
mangalist = mangaresults.find_all(class_= 'mangaresultinner')

mangaurls = []
mangatitles = []
mangatexts = [] 
for idx,item in enumerate(mangalist):
	mangaurls.append(item.find(class_='manga_name').find('a', href=True)['href'])
	mangatitles.append(item.find(class_='manga_name').h3.string)	
	mangatexts.append(item.find(class_='chapter_count').string)

print("======================================================")
print("Fetched results: ")
for idx,item in enumerate(mangaurls):
	print(str(idx+1) + '. ' + mangatitles[idx] + '\n\t\t - ' + mangatexts[idx])

chosen_idx = int(input("\nChose your Manga(enter the serial no.): ")) - 1
print("======================================================")

page = requests.get(URL + mangaurls[chosen_idx])
soup = BeautifulSoup(page.content, 'html.parser')

chapters = soup.find(id='listing').find_all('a', href=True)
chapterurls = []
for item in chapters:
	chapterurls.append(item['href'])

start_idx = int(input("Start Chapter: ")) - 1
end_idx = int(input("End Chapter: ")) - 1

print("======================================================")

chap = start_idx
page = requests.get(URL + chapterurls[chap])
soup = BeautifulSoup(page.content, 'html.parser')

pageurls = []
pages = soup.find(id='pageMenu').find_all('option', value=True)
for item in pages:
	pageurls.append(item['value'])

for purl in pageurls:  
	page = requests.get(URL + purl)
	soup = BeautifulSoup(page.content, 'html.parser')