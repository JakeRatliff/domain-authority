import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse
import re
import csv

URLs = [] #urls to get their backlinks

excludedDomains = [] #currently using just urlparse netloc, so its really using subdomains. TODO: make it more flexible.

headers = {"USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

print_to_csv = False #to print to file, change to true

if print_to_csv:
	print('\nprinting output to csv....\n')
	with open('extLinks.csv', 'a') as csvfile:
		fieldnames = ['URL', 'External Links']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
else:
	print('\n\n\n\n\n    ...Running in setup/debug mode. Change print_to_csv setting to print output to a csv file...\n\n\n\n\n')

def getExternals(url):
	try:
		domain = urlparse(url).netloc
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
					linkDomain = urlparse(href).netloc
					print(linkDomain, domain)
					if linkDomain is not domain:
						if linkDomain not in excludedDomains:
							print(url, href)
							if print_to_csv:
								with open('extLinks.csv', 'a') as csvfile:
									writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
									writer.writerow({'URL':url, 'External Links': href})
			except KeyError:
				print('\n...KeyError exception...\n')
	except KeyError:
		print('\n...some exception...\n')


for url in URLs:
	getExternals(url)
