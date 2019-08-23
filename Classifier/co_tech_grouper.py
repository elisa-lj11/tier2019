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

# CONSTANTS: change these to change source of key terms/phrases, source of company names, and source of company data to search
terms_list_filename = r'F:\Elisa\tf-idf_results\patent_4k_keyphrases.txt'
companies_list_filename = r'F:\Elisa\vr_companies.txt'
file_dir = r'F:\Elisa\text_files'
new_file_name = "co_tech_results.txt"
new_file = open(new_file_name, "w+", encoding="utf-8")
#word2vec_model_source = r"F:\Elisa\GoogleNews-vectors-negative300.bin\GoogleNews-vectors-negative300.bin"
#word2vec_model_source = r"F:\Elisa\inspect_word2vec-master\vocabulary"


results = dict()

current_file_count = 1
total_file_count = 0
for path,dirs,files in os.walk(file_dir):
    for file in files:
        if file.endswith(".txt"):
            total_file_count += 1

# FIXME: make this a dictionary with scores
terms_list = [line.rstrip('\n') for line in open(terms_list_filename, encoding='utf-8')]
companies_list = [line.rstrip('\n') for line in open(companies_list_filename, encoding='utf-8')]

for company in companies_list:
    results[company] = set()

for path,dirs,files in os.walk(file_dir):
    for n, file in enumerate(files):
        print("\rReading docs: " + str(current_file_count) + "/" + str(total_file_count),end=" ")
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
        current_file_count += 1
    
    print('\n',end="")

for key in results:
    new_file.write("{}:\n".format(key))
    for value in results[key]:
        new_file.write("{}\n".format(value)) 
    new_file.write("\n")

print("Done! Look for {} in the 'Classifier' directory".format(new_file_name))

#new_file.write(str(results))
#new_file.write(json.dumps(results))


# can use this model to find alike terms, doesn't work with company names
#model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_model_source, binary=True)
#model = api.load("glove-wiki-gigaword-100")
#result = model.most_similar(positive=companies_list)
#print(result[0])

