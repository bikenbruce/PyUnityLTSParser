import argparse
from bs4 import BeautifulSoup
import feedparser
import os
import requests

def local_version(debug, server_version):
	local_version_file = 'downloads/local_version.txt'
	# make directory if it does not exist
	if not os.path.isdir('downloads'):
		if debug: print('creating download directory')
		os.makedirs('downloads')

	# folder exists, but not file
	if not os.path.exists(local_version_file):
		if debug: print('creating local version file')
		f = open(local_version_file, 'w')
		f.write(server_version, "\n")
		f.close()
		# return

	else:
		# file and folder exists, open file, read content
		f = open(local_version_file, 'r')
		file_version = f.readline()
		if not file_version in server_version:
			if debug: print('local version does not match server version')
		else:
			if debug: print('local version does match server version')
		f.close()

		if debug: print('local:', file_version, 'server:', server_version)

def check_state(debug): 
	feed = feedparser.parse('https://unity3d.com/unity/lts-releases.xml')

	server_version = feed.entries[0]['title_detail']['value']
	summary = feed.entries[0]['summary_detail']['value']

	if debug: print('server version:', server_version)
	
	local_version(debug, server_version.strip())

	soup = BeautifulSoup(summary, 'lxml')

	tags = soup.find_all('a', href=True)

	for tag in tags:
		url = tag.get('href')
		if '.pkg' in url:
			file_name = url.rsplit('/', 1)[1]
			if debug: print(file_name)
		
			if not os.path.exists(file_name):
				pass
				#if debug: print('downloading: ', file_name)

			# r = requests.get(url)
			# open(file_name, 'wb').write(r.content)
		

if __name__ == "__main__":
	PARSER = argparse.ArgumentParser(description='Unity LTS check and download updates')
	PARSER.add_argument('-d', '--debug', help='debugging', action='store_true', default=False)
	ARGS = PARSER.parse_args()

	check_state(ARGS.debug)
