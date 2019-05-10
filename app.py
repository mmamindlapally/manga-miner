import requests
import os
import sys
import tempfile
import shutil
import img2pdf
from bs4 import BeautifulSoup

URL = "http://www.mangareader.net"
DDIR = "Downloads/"
if not os.path.exists(DDIR):
    os.makedirs(DDIR)
print("======================================================")
# ask for the manga
search_string = input("Enter your Manga: ")
search_string.replace(" ", "+")

# search for the manga
page = requests.get(URL + "/search/?w=" + search_string)
soup = BeautifulSoup(page.content, 'html.parser')

# show the results
mangaresults = soup.find(id = 'mangaresults')
mangalist = mangaresults.find_all(class_= 'mangaresultinner')

# make note of all the manga
mangaurls = []
mangatitles = []
mangatexts = [] 
for idx,item in enumerate(mangalist):
	mangaurls.append(item.find(class_='manga_name').find('a', href=True)['href'])
	mangatitles.append(item.find(class_='manga_name').h3.string)	
	mangatexts.append(item.find(class_='chapter_count').string)

print("======================================================")

# show the fetched manga
print("Fetched results: ")
for idx,item in enumerate(mangaurls):
	print(str(idx+1) + '. ' + mangatitles[idx] + '\n\t\t - ' + mangatexts[idx])

# ask to choose among them
chosen_idx = int(input("\nChose your Manga(enter the serial no.): ")) - 1
print("======================================================")

# Now open the chosen maga
TITLE = mangatitles[chosen_idx]
page = requests.get(URL + mangaurls[chosen_idx])
soup = BeautifulSoup(page.content, 'html.parser')

# note the href of all chapters
chapters = soup.find(id='listing').find_all('a', href=True)
chapterurls = []
for item in chapters:
	chapterurls.append(item['href'])

# ask for the starting and ending chapters
print(TITLE+ ": Chapters available from 1 to "+ str(len(chapterurls)))
start_idx = int(input("Start Chapter: ")) - 1
end_idx = int(input("End Chapter: ")) - 1

# check if he/she/it is messing with you ^^
if(start_idx>end_idx or end_idx>=len(chapterurls)):
	print("Invalid!!!")
	exit()

print("======================================================")

# for each chapter asked for
for chap in range(start_idx, end_idx+1):

	CHTITLE = TITLE + " " + str(chap+1);
	page = requests.get(URL + chapterurls[chap])
	soup = BeautifulSoup(page.content, 'html.parser')

	# note all the page urls and the imgurls
	pageurls = []
	imgurls = []
	imglocs = []
	pages = soup.find(id='pageMenu').find_all('option', value=True)
	for item in pages:
		pageurls.append(item['value'])
	for purl in pageurls:  
		page = requests.get(URL + purl)
		soup = BeautifulSoup(page.content, 'html.parser')
		imgurls.append(soup.find(id='img')['src'])

	# download all the images to a temporary directory
	for pidx, iurl in enumerate(imgurls):
		img_data = requests.get(iurl).content
		fname = str(idx) + '.jpg'
		tmpdir = tempfile.mkdtemp()

		path = os.path.join(tmpdir, fname)
		try:
			# update the user of download progress
			sys.stdout.write('%s: Downloading Page: %s of %s\r' % (CHTITLE, str(pidx+1), str(len(imgurls))))
			sys.stdout.flush()

			with open(path, "wb") as tmp:
				tmp.write(img_data)

			imglocs.append(path)

		except IOError as e:
			print('IOError in page ' + str(pidx+1))

	# convert all the downloaded images to pdf
	pdfname = os.path.expanduser(DDIR) + CHTITLE.replace(' ', '_') +".pdf"
	with open(pdfname, "wb") as f:
		f.write(img2pdf.convert([i for i in imglocs if i.endswith(".jpg")]))
		sys.stdout.write("%s FINISHED :D                      \n" % (CHTITLE))
		sys.stdout.flush()

	# remove the download directory
	shutil.rmtree(tmpdir)

# :D :D :D 
print("======================================================")
print("                     THANK YOU                        ")
print("======================================================")
