import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse
import re
import csv

URLs = [] #urls to get their backlinks

excludedDomains = [] #not really

headers = {"USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

with open('extLinks.csv', 'a') as csvfile:
	fieldnames = ['URL', 'External Links']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

def getExternals(url):
	try:
		print(url, '\n\n')
		externalLinks = []
		page = requests.get(url, headers=headers).text
		soup = BeautifulSoup(page, "html.parser")
		links = soup.findAll("a", href=re.compile("^(http|www)"))
		#print(links)
		for link in links:
			try:
				if link.attrs['href'] is not None:
					href = link.attrs['href']
					domain = urlparse(href).netloc
					if domain not in excludedDomains:
						print(url, href)
						with open('extLinks.csv', 'a') as csvfile:
							writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
							writer.writerow({'URL':url, 'External Links': href})
			except KeyError:
				print('\n...KeyError exception...\n')
	except KeyError:
		print('\n...some exception...\n')


for url in URLs:
	getExternals(url)
