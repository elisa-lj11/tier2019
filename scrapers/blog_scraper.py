# Uses an HTML parser to scrape blogs for comments
# Created by Elisa Lupin-Jimenez

import os
from html.parser import HTMLParser
from bs4 import BeautifulSoup

new_file = open(r"C:\Users\d33914\Documents\blogs_text\text_files\scraped_blog.txt", "w+", encoding="utf-8")

# Change this to read from a specific directory
d = r'C:\Users\d33914\Documents\blogs_text\avforums_steam_outselling_oculus\www.avforums.com\threads'

# class parsePost(HTMLParser):
#     def handle_data(self, data):
#         count = 0
#         for line in data:
#             if 'class="messageContent' in line:
#                 count += 1
#                 print(count)
#                 #print(line)
            
#         #print(data)

#parser = parsePost()

for path,dirs,files in os.walk(d):
    for file in files:
        if file.endswith('div.html'):
            continue
        try:
            with open(os.path.join(path,file),'r',encoding='utf-8') as f:
                html_contents = f.read()
                soup = BeautifulSoup(html_contents, features='lxml')
                #print(soup.prettify())
                #print(html_contents)
                for tag in soup.find_all('blockquote', 'messageText'):
                    new_file.write("{}\n\n".format(tag))
                    #print(tag.contents)
                #print(html_as_text)
                # BS = BSHTML(html_contents)
                # for line in html_code_list:
                #     line = line.strip()
                #     if 'class="messageContent"' in line:
                #         new_file.write("\n\n{}".format(line))
                #parser.feed(html_contents)
                #parser.close()
                #HTMLParser.feed(f)
                #text = f.read()
        except:
            print("Unable to write to file")
            continue
        if html_contents == None or html_contents == '':
            print("Empty HTML file")
            continue
        #text_list.append(text)
