# Created by Elisa Lupin-Jimenez

import os
#from html.parser import HTMLParser
from bs4 import BeautifulSoup
#from selectolax.parser import HTMLParser

# Change this to read data from a specific directory
source_dir = r'F:\Elisa\text_files\avforums_text_files'

#Change this to write results to a specific directory
result_dir = r'F:\Elisa\text_files\avforums_text_files_cleaned'

def get_text_bs(html):
    tree = BeautifulSoup(html, 'lxml')

    body = tree.body
    if body is None:
        return None

    for tag in body.select('script'):
        tag.decompose()
    for tag in body.select('style'):
        tag.decompose()

    text = body.get_text(separator='\n')
    return text

for path,dirs,files in os.walk(source_dir):
    for file in files:
        if file.endswith('div.html'):
            continue
        try:
            with open(os.path.join(path,file),'r',encoding='utf-8') as f:
                new_file_name = result_dir + '\\' + file
                print(new_file_name)
                new_file = open(new_file_name, "w+", encoding="utf-8")
                html_contents = f.read()
                #text = get_text_selectolax(html_contents)
                text = get_text_bs(html_contents)
                new_file.write(text)
                #soup = BeautifulSoup(html_contents, features='lxml')
                #print(soup.prettify())
                #print(html_contents)
                #for tag in soup.find_all('blockquote', 'messageText'):
                    #new_file.write("{}\n\n".format(tag))

        except:
            print("Unable to write to file")
            continue
        if html_contents == None or html_contents == '':
            print("Empty HTML file")
            continue
        #text_list.append(text)
