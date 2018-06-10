import json
import sys
import time
from bs4 import BeautifulSoup


def check_tags(soup, tag_name, peek_max):
	tags = soup.findAll(tag_name)
	print('\n'.join([stub.text.strip()[:peek_max] for stub in tags]))
	print()

# def extract_tag_by_index(soup, tag_name, ind):
# 	print('Extracting obfuscated scripts')

# 	tags = soup.findAll(tag_name)

# 	if ind < 0:
# 		ind = len(tags) + ind

# 	i = 0
# 	for tag in tags:
# 		if i == ind:
# 			tag.extract()

# 	print(tags)
# 	return soup


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

def extract_SLConfig(soup):
	print('Extracting SLConfig')

	scripts = soup.findAll('script')

	# if reveal export, -2
	# if html export, -3
	config = str(scripts[-2].contents[0])

	start = config.find('{')
	end = len(config) - config[::-1].find('}')

	jsone = json.loads(config[start:end]) # dict(config[start:end])
	json_1 = jsone['deck']

	json_2 = dict()
	json_2['deck'] = {
		'width': 				 json_1['width'],
		'height': 				 json_1['height'],
		'share_notes': 			 json_1['share_notes'],
		'slide_number': 		 json_1['slide_number'],
		'auto_slide_interval': 	 json_1['auto_slide_interval'],
		'center': 				 json_1['center'],
		'shuffle': 				 json_1['shuffle'],
		'should_loop': 			 json_1['should_loop'],
		'rtl': 					 json_1['rtl'],
		'transition': 			 json_1['transition'],
		'background_transition': json_1['background_transition']
	}

	replace_tag = soup.new_tag('script')
	replace_tag.string = config[:start] + json.dumps(json_2) + config[end:]
	scripts[-2].replace_with(replace_tag)
	# scripts[-2].replaceWithChildren()
	print(replace_tag)

	return soup

def extract_obfuscated_stylesheets(soup):
	print('Extracting obfuscated stylesheets')
	styles = soup.findAll('style') # , attrs={'class': 'name'}

	check_tags(soup, 'style', 18)

	for style in styles:
		# print(style.text.strip()[:18], end='\n')
		style.extract()

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


	soup = extract_SLConfig(soup)
	# soup = extract_obfuscated_scripts(soup)
	# check_tags(soup, 'script', 18)

	soup = extract_obfuscated_stylesheets(soup)
	check_tags(soup, 'style', 18)


	timestamp = int(time.time())
	if source[::-1].find('/') == -1:
		folder = '.'
	else:
		folder = source[:-source[::-1].find('/') + len(source)]

	with open('%s/export-%s.html' % (folder, timestamp), 'w') as outfile:
		# if not using prettify w formatter,
		# indents like &nbsp; will be escaped and/or transformed to unicode
		outfile.write(str(soup.prettify(formatter='html')))
		print('Saved to file !')
