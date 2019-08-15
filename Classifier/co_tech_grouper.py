# created by Elisa Lupin-Jimenez
#
# step 1
#   Get key terms list from TF-IDF
# step 2
#   get company names list from word2vec, fortune500, etc for category labels
# step 3
#   search through each chunk of each document to categorize chunks by company then
#       fit key terms into company category
# step 4
#   produce results of categorization
# additional details
#   - rank key terms for each company (based on TF-IDF and on frequency within company)
#   - swap company for key terms as categories
#   - use word2vec to gather more companies/key terms

import nltk
import string
import gensim
import csv
import json
import os
import gensim.downloader as api

results = dict()
new_file = open("co_tech_results.txt", "w+", encoding="utf-8")

terms_list_filename = r'F:\Elisa\tf-idf_results\patent_150k_keyphrases.txt'
companies_list_filename = r'F:\Elisa\vr_companies.txt'
#word2vec_model_source = r"F:\Elisa\GoogleNews-vectors-negative300.bin\GoogleNews-vectors-negative300.bin"
#word2vec_model_source = r"F:\Elisa\inspect_word2vec-master\vocabulary"
file_dir = r'F:\Elisa\text_files'

# FIXME: make this a dictionary with scores
# FIXME: cut down on number of terms for now
terms_list = [line.rstrip('\n') for line in open(terms_list_filename, encoding='utf-8')]
#for term in terms_list:
    #print("Reading term: {}\n".format(term))
#print(terms_list)
companies_list = [line.rstrip('\n') for line in open(companies_list_filename, encoding='utf-8')]
#print(companies_list)

for company in companies_list:
    results[company] = set()

for path,dirs,files in os.walk(file_dir):
    for n, file in enumerate(files):
        print("\rReading docs: " + str(n+1) + "/" + str(len(files)),end=" ")
        if not file.endswith('.txt'):
            continue
        try:
            with open(os.path.join(path,file),'r',encoding='utf-8') as f:
                text = f.readlines()
                #print(text)
        except:
            continue
        if text == None or text == '':
            continue
        #split text into paragraphs
        for line in text:
            line = line.lower()
            # why is it printing the line char by char?
            #print(line)
            for term in terms_list:
                #print("Reading term %s\n".format(term))
                if term in line:
                    #print("found a term!")
                    for company in companies_list:
                        #print("company")
                        # FIXME: check for company name in filename
                        if company.lower() in line:
                            #print("found a company term match!")
                            results[company].add(term)
                            #print("added {} to {} bank".format(term, company))
    print('\n',end="")

for key in results:
    new_file.write("{}:\n".format(key))
    for value in results[key]:
        new_file.write("{} \n".format(value)) 
    new_file.write("\n")

#new_file.write(str(results))
#new_file.write(json.dumps(results))


# can use this model to find alike terms, doesn't work with company names
#model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_model_source, binary=True)
#model = api.load("glove-wiki-gigaword-100")
#result = model.most_similar(positive=companies_list)
#print(result[0])

