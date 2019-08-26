## New contributions by Elisa Lupin-Jimenez, GitHub @elisa-lj11

### Files added for summer 2019:
- Classifier/co_tech_compare.py
	- To find common key phrases between companies
- Classifier/co_tech_grouper.py
	- To find the top relevant key phrases associated with a list of companies
- Classifier/rank_keyphrase.py
	- To assign scores to key phrases within/between documents
- scrapers/blog_scraper.py
	- To pull posts/comments from raw HTML files
- scrapers/blog_url_list_generator.py
	- To use with HTTRack, an application that downloads website code
- scrapers/csv_to_text.py
	- To convert columns of a csv file to a txt file
- twitter_api/tweepy/download_tweet.py
	- To download tweets from an account (need API key)
- twitter_api/twitter_search/twitterSearch.py
	- To download tweets with specified phrases (need API key)

### ORDER OF USE:
1. Collect your data (in .txt format)
	- use blog_scraper.py to get data from forums
	- use the twitter scripts to get Twitter data (not super useful from my experience)
	- use csv_to_text.py to convert patent files to txt files for later use
2. Run rank_keyphrase.py
	- collect your .txt files into one directory
	- will output a new .txt file with the scores of keywords for each document
3. Run co_tech_grouper.py
	- will use your ranked keyphrases (must not include scores in order to work) .txt file
	- will use a company name .txt file (list of companies you have data for)
	- will output a new .txt file that lists each company followed by key phrases associated with that company
4. Run co_tech_compare.py
	- input two company names based on the data that you have/want to compare
	- will use the output of co_tech_grouper.py to produce a list that compares shared key phrases between two companies

------------------------------
This collection of files was created in summer 2018 for use at 台灣經濟研究院. 
For questions of use please contact Patrick via github/stackoverflow, open an issue, or use his hotmail: patrick t oneil.

-Analysis_tools contains files for text analysis, including word2vec, a 'most common bigrams' extractor, and a company extractor based on NER tags.
-Scrapers contains files for scraping articles from news sites, and for scraping company financial reports.
-txt_conversion contains files for converting .doc and .pdf files to .txt format, using LibreOffice and pdfminer respectively.
-Burst_detection contains files for burst detection based on the python package and methodology by nmarinsek (based off Kleinenberg's paper)
-Classifier contains a file for Latent Dirichlet analysis, and a file for classifying companies into low, medium and high digital maturity categories based off their financial reports.




INSTRUCTIONS FOR USE OF APP.PY
------------------------------

You must have Google Chrome downloaded on your computer.

If this file did not come with chromedriver.exe, download it now
and put it in the same folder with these files:
http://chromedriver.chromium.org/downloads

I recommend having one folder with 'app.exe', 'chromedriver.exe', 
and this 'README.txt' in it.

There is an issue downloading some pdfs from oecd-ilibrary.org that has
not been solved as of 14 August 2018 which causes them to be unreadable.
To run the program, simply double-click on 'app.exe'. You may have
to right-click and select 'run as administrator' to get it to work.
When done, please press 'Quit', as it will close everything.


      使用說明
-------------------

你必須在計算機上下載Google Chrome。

如果此文件未附帶chromedriver.exe，請立即
下載並將它與這些文件放在同一個文件夾中：
http://chromedriver.chromium.org/downloads

你應該有一個帶有'app.exe'、'chromedriver.exe'、
和這個'README.txt'的文件。

要運行該程序，只需雙擊'app.exe'即可。 你可能有
右鍵單擊並選擇'以系統管理員身分執行'以使其正常工作。
完成後，請按'退出'。#