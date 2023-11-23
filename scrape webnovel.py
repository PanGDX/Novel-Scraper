from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager


output_file = str(input("Output file: "))
url_to_scrape = str(input("Url of the chapter: "))
content = str(input("A part of the content of the chapter: "))
link_text = str(input("The text leading to the next chapter: "))
chapter_number = int(input("Chapter number: "))
encoding_type = str(input("Encoding types (default utf-8)\n(Alternative option: gbk):"))
if(encoding_type == ""): encoding_type = "utf-8"





def formatting(next_link):
	
	if "http" in next_link:
		return next_link
	else:
		bracketposition = url_to_scrape.find('/', url_to_scrape.find('//') + 2)
		return url_to_scrape[:bracketposition] + next_link
	
def append_file(content):
	with open(f'C:\Users\Pran\Desktop\patreon\input files\{output_file}.txt', 'a', encoding= encoding_type) as files:
		files.write(content)
		files.write("\nNEWCHAPTERNEWCHAPTERNEWCHAPTERNEWCHAPTERNEWCHAPTERNEWCHAPTERNEWCHAPTER\n\n\n")
		files.close()


def find_divs_with_text(soup, search_text): #return whatever it finds
	search_text = search_text.strip()
	# Find all 'div' tags that contain the search_text
	divs = soup.find_all(lambda tag: tag.name == 'div' and search_text in tag.text)

	# Collect the class and id attributes of each div
	results = []
	tag_class = ""
	tag_id = ""

	for div in divs:
		tag_class = ' '.join(div.get('class', []))  # Get class as a space-separated string
		tag_id = div.get('id', '')  # Get id
		results.append((tag_class, tag_id))

	return tag_class, tag_id

def get_link(soup, text): #return False for error

	text = text.lower()
	
	text_array = text.split(" ")
	
	for search_text in text_array:
	
		#print(search_text)
		if search_text == "":
			return False
		
		counter = 0
		while counter<=4:
			matchedtags = soup.find_all(lambda tag: len(tag.find_all()) == counter and search_text in tag.text.lower())
			
			
			

			if matchedtags:
				
				for tag in matchedtags:
					
					tag_type = tag.name
				
					if tag_type == 'a':
						return tag.get('href')

			counter+=1  
	
	raise ValueError(f"Failed to fetch the link with the link-text given")

def get_page_encoding(soup):
		# Get the page encoding
	meta_charset = soup.meta.get('charset')
	if meta_charset is None:
		meta_charset = soup.meta.get('content-type')
		if meta_charset is None:
			meta_charset = soup.meta.get('content')
	if meta_charset and 'charset=' in meta_charset:
			meta_charset = meta_charset.split('charset=')[-1]# Correct the charset if necessary
	if meta_charset == 'gb2312':
		meta_charset = 'gbk'

	return meta_charset

def create_selenium_driver():
	# Setup Firefox options
	firefox_options = Options()
	firefox_options.add_argument("--headless")  # Ensures the browser window doesn't pop up

	# Initialize the driver with the Service object
	service = Service(executable_path=GeckoDriverManager().install())
	driver = webdriver.Firefox(service=service, options=firefox_options)

	return driver


def scrape_webpage(driver, url, link_text, content_class, content_id, chapter_number):
	try:
		# Navigate to the initial URL
		driver.get(url)
		page_source = driver.page_source
		
		soup = BeautifulSoup(page_source, 'html.parser',  from_encoding= encoding_type)
		
		result = f"Chapter {chapter_number}"
		chapter_number+=1

		for content in soup.find_all('div', class_=content_class, id=content_id):
			result += content.get_text() + '\n'
		append_file(result)
		

		next_link = get_link(soup, link_text)

		if next_link:
			print(f"Navigating to the next link: {next_link}")
			next_link = formatting(next_link)
			scrape_webpage(driver, next_link, link_text, content_class, content_id, chapter_number)
		else:
			print("No next link found, or there was an error fetching it.")

	except Exception as e:
		print(f"An error occurred: {e}")

def access_website_with_selenium():
	driver = create_selenium_driver()

	
	driver.get(url_to_scrape)

	page_source = driver.page_source
	soup = BeautifulSoup(page_source, 'html.parser')
		

	#encoding = get_page_encoding(soup)

	# Find divs with text
	
	content_class, content_id = find_divs_with_text(soup, content)
		
	# Get the link for the next page

	

	#number_of_chapters = int(input("Number of chapters: "))
	
	scrape_webpage(driver, url_to_scrape, link_text, content_class, content_id, chapter_number)
	#is recursive

	driver.quit()  # Ensure the driver is quit properly

# You would call the function with the URL, content_text, and link_text as before

try:
	if __name__ == "__main__":
  # You'll need to add this input to get the link_text
		with open(f'C:\Users\Pran\Desktop\patreon\input files\{output_file}.txt', 'w') as files:
			files.write("") #clears file

		access_website_with_selenium()
except Exception as e:
	print(e)
	input_ = input()

#chapter number unused
