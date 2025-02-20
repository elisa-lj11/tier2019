# -*- coding: utf-8 -*-

# Patrick O'Neil 2018
########################################################################################################
# NOTES: 	engadget and 36kr load with javascript, which is why a headless browser is necessary.
#			verge is anti-scraping, the header is copy-pasted from visiting it manually. The time.sleep 
#				is there to keep from getting banned.
#			techcrunch doesn't have any 'pages' of results, so we can only get ~20 results max.
#
#			There seems to be a large potential for bugs if chrome doesn't load fast enough. I don't know
#			how to test this, and implementing seems tedious and I'd be trying to fix a leak in the dark.


from bs4 import BeautifulSoup as BS
from selenium import webdriver
import time, requests, os

egt_home = 'http://www.engadget.com'
kr_home = 'http://www.36kr.com'
tc_search_addr = 'http://www.techcrunch.com/search/'
verge_search_addr = 'https://www.theverge.com/search?page='
verge_sep = '&q='
egt_search_addr = 'https://www.engadget.com/search/?search-terms='
url_1_36kr = 'http://www.36kr.com/search/articles/'
url_2_36kr = '?page='
url_3_36kr = '&ts=1531173711595'
DGT_username = 'd17635@tier.org.tw'
DGT_password = 'rebeca1'
DGT_site = 'http://www.digitimes.com.tw'
oecd_home = "http://www.oecd.org"
oecd_1 = "http://www.oecd.org/general/searchresults/?q="
oecd_2 = "&cx=012432601748511391518:xzeadub0b0a&cof=FORID:11&ie=UTF-8"

# Turns out after forgetting to change which one I used, it doesn't matter - as long as it's a valid header.
verge_mac_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
verge_pc_header =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}


#Gets all resultant article links for a given search term on techcrunch.com. 
def get_TC_art_links(term):
	link_list = []
	url = tc_search_addr + term
	html = requests.get(url).text
	soup = BS(html,'lxml')
	all_arts_class = soup.findAll('a', attrs={'class':'post-block__title__link'})
	for item in all_arts_class:
		link = item.attrs['href']
		link_list.append(link)
	return link_list

def get_TC_art_text(link):
	html = requests.get(link).text
	soup = BS(html,'lxml')
	art = soup.find('div',attrs={'class':'article-content'})
	if not art:
		art = soup
	text = ''
	for p in art.findAll('p'):
		text = text + ' ' + p.text
	return text

#Gets all resultant article links for a given search term on engadget.com.
#Opens a browser via selenium's webdriver and clicks on the 'Show more results' for every page.
def get_EGT_art_links(term,pages,chrome):
	link_list = []
	url = egt_search_addr + term
	chrome.get(url)
	time.sleep(2)
	print("\rPage " + str(1),end="")
	for i in range(pages - 1):
		try:
			more_res_link = chrome.find_element_by_link_text("Show more results")
			more_res_link.click()
		except:
			break
		pageno = i + 2
		print("\rPage " + str(pageno),end="")
		time.sleep(3)
	html = chrome.page_source
	soup = BS(html, 'lxml')
	all_arts_class = soup.findAll('a', attrs={'class':'o-hit__link'})
	for item in all_arts_class:
		link = item.attrs['href']
		link = egt_home + link
		link_list.append(link)
	return link_list

def get_EGT_art_text(link):
	html = requests.get(link).text
	soup = BS(html,'lxml')
	art = soup.find('div',attrs={'class':'flush-top flush-bottom'})
	if not art:
		art = soup
	text = ''
	for p in art.findAll('p'):
		text = text + ' ' +p.text
	return text

#Gets all resultant article links for the first 30 pages on theverge.com.
def get_verge_art_links(term,pages):
	link_list = []
	for i in range(pages):
		pageno = i + 1
		print("\rPage " + str(pageno),end="")
		url = verge_search_addr + str(pageno) + verge_sep + term
		text = requests.get(url,headers=verge_pc_header).text
		time.sleep(1)
		soup = BS(text,'lxml')
		all_arts_class = soup.findAll('a',attrs={'data-analytics-link':'article'})
		if not all_arts_class:
			break
		for item in all_arts_class:
			link = item.attrs['href']
			link_list.append(link)
		time.sleep(1)
	return link_list

def get_verge_art_text(link):
	html = requests.get(link,headers=verge_mac_header).text
	soup = BS(html,'lxml')
	art = soup.find('div',attrs={'class':'c-entry-content'})
	if not art:
		art = soup
	text = ''
	for p in art.findAll('p'):
		text = text + ' ' + p.text
	return text

def get_36kr_art_links(term,pages,chrome):
	link_list = []
	for i in range(pages):
		pageno = i + 1
		print("\rPage " + str(pageno),end="")
		url_search = url_1_36kr + term + url_2_36kr + str(pageno) + url_3_36kr
		try:
			chrome.get(url_search)
		except:
			print("\nPage " + str(pageno) + " couldn't be loaded.")
			continue
		html = chrome.page_source
		soup = BS(html,'lxml')
		results = soup.find('div',attrs={'class':'search-list-panel list-column-one'})
		while not results:
			if soup.find('div',{'class':'no-result-box'}) != None:
				return link_list
			print('\rWaiting...',end="")
			time.sleep(3)
			print('...',end="")
			html = chrome.page_source
			soup = BS(html,'lxml')
			results = soup.find('div',attrs={'class':'search-list-panel list-column-one'})
		result_links = results.findAll('a')
		for link in result_links:
			art_link = kr_home + link.attrs['href']
			link_list.append(art_link)
	return link_list

def get_36kr_art_text(link,chrome):
	text = ''
	try:
		chrome.get(link)
	except:
		print('exception thrown. probably a timeout')
		chrome.get('http://www.36kr.com')
		return text
	html = chrome.page_source #TODO: wait until it's loaded
	soup = BS(html,'html5lib')
	try:
		art = soup.find('section',attrs={'class':'textblock'})
		for p in art.findAll('p'):
			text = text + ' ' + p.text
		return text
	except:
		return text

def get_DGT_art_links(term,pages,chrome):
	link_list = []
	chrome.get(DGT_site)
	search_bar = chrome.find_element_by_id('query')
	search_bar.clear()
	search_bar.send_keys(term + '\n')
	for i in range(pages):
		pageno = i + 1
		print("\rPage " + str(pageno),end="")
		time.sleep(3) 
		html = chrome.page_source
		soup = BS(html,'html5lib') #Digitimes' html is often malformed, so using lxml makes the parsing stop before we get the whole page.
		results = soup.findAll('input',{'type':'checkbox'})
		while not results:
			print('Waiting...')
			time.sleep(3)
			html = chrome.page_source
			if html.find('找不到符合所輸入關鍵字的報導，建議您調整查詢的邏輯後再試看看') != -1:
				return []
			soup = BS(html,'html5lib')
			results = soup.findAll('input',{'type':'checkbox'})
		for obj in results:
			link = DGT_site + obj['url']
			link_list.append(link)
		try:
			nextpage = chrome.find_element_by_link_text(str(pageno+1))
			nextpage.click()
		except:
			break
	return link_list

def get_DGT_art_text(link,chrome):
	chrome.get(link)
	html = chrome.page_source
	soup = BS(html,'html5lib')
	time.sleep(1)
	if soup.find('form',{'id':'Login'}): #TODO: Should I check if it's even loaded?
		user = chrome.find_element_by_name('checkid')
		pwd = chrome.find_element_by_name('checkpwd')
		user.send_keys(DGT_username)
		pwd.send_keys(DGT_password)
		pwd.submit()
		time.sleep(1)
	html = chrome.page_source
	soup = BS(html,'html5lib')
	pars = soup.findAll('p',attrs={'class':'main_p'})
	text = ''
	for p in pars:
		text = text + p.text
	return text

def get_OECD_art_links(term,pages,chrome):
	link = oecd_1 + term + oecd_2
	chrome.get(link)
	if pages >= 10:
		pages = 10
	links = []
	for i in range(pages):
		pageno = i + 1
		print("\rPage " + str(pageno),end="")
		time.sleep(2)
		html = chrome.page_source
		soup = BS(html,'lxml')
		link_objs = soup.findAll('div',{'class':'gsc-webResult gsc-result'})
		for l in link_objs:
			links.append(l.find('a')['href'])
		pages_list = chrome.find_elements_by_class_name('gsc-cursor-page')
		if pageno >= len(pages_list):
			break
		else:
			pages_list[pageno].click() # the array starts from 0, we want the next page, pageno starts at 1, so we can just get [pageno]
	chrome.quit()
	pdf_link_list = []
	print("\nGetting all pdf links...")
	for link in links:
		#looks like it doesn't handle oecd-ilibrary correctly. could have something to do w a redirect but it doesn't look like it.
		if link.endswith('pdf'):
			pdf_link_list.append(link)
		else:
			temp_html = requests.get(link).text
			temp_soup = BS(temp_html,'lxml')
			temp_links = temp_soup.findAll('a')
			for t in temp_links:
				try:
					l = t['href']
					if l.endswith('pdf'):
						pdf_link_list.append(l)
						break
				except:
					continue
	return pdf_link_list

def save_OECD_links(link_list,language,term):
	if language == 'en':
		language = 'english'
	elif language == 'zh':
		language = 'simplified'
	elif language == 'zh_Hant':
		language = 'traditional'
	for i,link in enumerate(link_list):
		print("\r" + str(i+1) + "/"+str(len(link_list)),end="")
		if not link.endswith('pdf'):
			continue
		if not link.startswith('http'):
			link = oecd_home + link
		filename = sterilize_link(link)
		r = requests.get(link,allow_redirects=True,timeout=10)
		try:
			with open('{}/{}/{}.pdf'.format(language,term,filename),'wb') as output:
				output.write(r.content)
		except:
			os.makedirs('{}/{}'.format(language,term))
			with open('{}/{}/{}.pdf'.format(language,term,filename),'wb') as output:
				output.write(r.content)

#Sterilizes the link so it can be used as a (unique) filename.
def sterilize_link(link):
	link = link.replace('http://','')
	link = link.replace('https://','')
	link = link.replace('/','-')
	replace = ['.com','www.','.tw','.html','&','.',',','?','!','%','#','=','+', '\\']
	for r in replace:
		link = link.replace(r,'')
	return link

def sterilize_term(term): #Not sure I actually need this function.
	term = term.replace('\\','')
	term = term.replace('/','')
	return term

def save_art_texts(language,term,link_text_dict):
	term = sterilize_term(term)
	for link in link_text_dict.keys():
		filename = sterilize_link(link)
		try:
			with open('{}/{}/{}.txt'.format(language,term,filename),'w',encoding='utf-8') as output:
				text = link_text_dict[link]
				if not text:
					continue
				output.write(text)
		except:
			os.makedirs('{}/{}'.format(language,term))
			with open('{}/{}/{}.txt'.format(language,term,filename),'w',encoding='utf-8') as output:
				text = link_text_dict[link]
				if not text: #could also do this check when creating the dict
					continue
				output.write(text)