from bs4 import BeautifulSoup
import feedparser
from os import path
import requests

def current_version(version):
	if path.exists(version):
		print('does not exist')
	else:	
		print('does exists')

feed = feedparser.parse('https://unity3d.com/unity/lts-releases.xml')

summary = feed.entries[0]['summary_detail']['value']
version = feed.entries[0]['title_detail']['value']

print(version)

current_version(version)

soup = BeautifulSoup(summary, 'lxml')

tags = soup.find_all('a', href=True)

for tag in tags:
	url = tag.get('href')
	if '.pkg' in url:
		file_name = url.rsplit('/', 1)[1]
		# print(file_name)
		
		if not path.exists(file_name):
			print('downloading: ', file_name)

		# r = requests.get(url)
		# open(file_name, 'wb').write(r.content)
		
