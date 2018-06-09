import sys
import time
from bs4 import BeautifulSoup


def check_tags(soup, tag_name, peek_max):
	tags = soup.findAll(tag_name)
	print('\n'.join([stub.text.strip()[:peek_max] for stub in tags]))
	print()

def extract_obfuscated_scripts(soup):
	print('Extracting obfuscated scripts')
	scripts = soup.findAll('script') # , attrs={'class': 'name'}

	# first script is user data/config,
	# last script is Reveal.initialize
	# check_tags(soup, 'script', 18)

	# print(type(scripts[0])) #Tag

	for script in scripts[1:-1]:
		# print(script.text.strip()[:18], end='\n')
		script.extract()
	
	print()

	return soup

def extract_obfuscated_stylesheets(soup):
	print('Extracting obfuscated stylesheets')
	styles = soup.findAll('style') # , attrs={'class': 'name'}

	check_tags(soup, 'style', 18)

	for style in styles:
		# print(style.text.strip()[:18], end='\n')
		style.extract()
	
	print()

	return soup

if __name__ == '__main__':
	if len(sys.argv) > 1:
		source = sys.argv[1]
	else:
		print('No file provided !')
		exit()

	with open(source, 'r') as page:
		print('Parsing file: %s\n' % source)
		soup = BeautifulSoup(page, 'html.parser')


	soup = extract_obfuscated_scripts(soup)
	check_tags(soup, 'script', 18)

	soup = extract_obfuscated_stylesheets(soup)
	check_tags(soup, 'style', 18)

	timestamp = int(time.time())

	folder = source[:-source[::-1].find('/') + len(source)]
	with open('%s/export-%s.html' % (folder, timestamp), 'w') as outfile:
		outfile.write(str(soup))
