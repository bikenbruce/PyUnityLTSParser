import argparse
from bs4 import BeautifulSoup
import feedparser
import os
import requests

def local_version(debug, server_version):
	# method that checks the local version of unity to the server version.
 	# returns true if local matches remote, returns false if not matched.

	local_version_file = 'downloads/local_version.txt'
	# make directory if it does not exist
	if not os.path.isdir('downloads'):
		print('creating download directory')
		os.makedirs('downloads')

	# folder exists, but not file
	if not os.path.exists(local_version_file):
		print('creating local version file')
		f = open(local_version_file, 'w')
		f.write(server_version)
		f.close()
		return(False)

	else:
		# file and folder exists, open file, read content
		f = open(local_version_file, 'r')
		file_version = f.readline()
		if debug: print('local version: ', file_version)
		if not file_version in server_version:
			print('local version does not match server version')
			f.close()
	
			print('updating local version')
			f = open(local_version_file, 'w')
			f.write(server_version)
			f.close()
			return(False)

		else:
			print('local version matches server version')
			f.close()
			return(True)

def check_state(debug): 
	feed = feedparser.parse('https://unity3d.com/unity/lts-releases.xml')

	server_version = feed.entries[0]['title_detail']['value']
	summary = feed.entries[0]['summary_detail']['value']

	if debug: print('server version:', server_version)
	
	local_state = local_version(debug, server_version.strip())

	if not local_state:
		soup = BeautifulSoup(summary, 'lxml')

		tags = soup.find_all('a', href=True)

		for tag in tags:
			url = tag.get('href')
			if '.pkg' in url:
				file_name = url.rsplit('/', 1)[1]
				if debug: print("url: ", url)
				if debug: print("file_name:", file_name)
		
				if not os.path.exists(file_name):
					print('downloading: ', file_name)

					r = requests.get(url)
					open('downloads/' + file_name, 'wb').write(r.content)
		

if __name__ == "__main__":
	PARSER = argparse.ArgumentParser(description='Unity LTS check and download updates')
	PARSER.add_argument('-d', '--debug', help='debugging', action='store_true', default=False)
	ARGS = PARSER.parse_args()

	check_state(ARGS.debug)
