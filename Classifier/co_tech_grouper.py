# created by Elisa Lupin-Jimenez
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
import gensim.downloader as api


terms_list = r'F:\Elisa\tf-idf_results\patent_keyphrase_weighting.txt'
companies_list_filename = r'F:\Elisa\vr_companies.txt'
word2vec_model_source = r"F:\Elisa\GoogleNews-vectors-negative300.bin\GoogleNews-vectors-negative300.bin"
#word2vec_model_source = r"F:\Elisa\inspect_word2vec-master\vocabulary"
file_dir = r'F:\Elisa\text_files'

companies_list = [line.rstrip('\n') for line in open(companies_list_filename, encoding='utf-8')]
#print(companies_list)


# can use this model to find alike terms, doesn't work with company names
#model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_model_source, binary=True)
#model = api.load("glove-wiki-gigaword-100")
#result = model.most_similar(positive=companies_list)
#print(result[0])





# # Load training data
# f = open(r'F:\Elisa\text_files\vr-patent-reports\CSV1907171053-train.csv', newline='', encoding='utf-8')
# train_rows = [row for row in csv.reader(f)][1:]
# random.shuffle(train_rows)
# patents_train = [row[0].decode('utf8') for row in train_rows]
# classes_train = [row[1] for row in train_rows]

# # Load testing data
# f = open(r'F:\Elisa\text_files\vr-patent-reports\CSV1907171053.csv', newline='', encoding='utf-8')
# test_rows = [row for row in csv.reader(f)][1:]  # discard the first row
# patents_test = [row[0].decode('utf8') for row in test_rows]
# classes_test = [row[1] for row in test_rows]



# tried using code from https://monkeylearn.com/blog/beginners-guide-text-vectorization/
# didn't work because it couldn't decode, or find load_model

#import random
#import skipthoughts
# class SkipThoughtsVectorizer(object):
#     def __init__(self, **kwargs):
#         self.model = skipthoughts.load_model()
#         self.encoder = skipthoughts.Encoder(self.model)
 
#     def fit_transform(self, raw_documents, y):
#         return self.encoder.encode(raw_documents, verbose=False)
 
#     def fit(self, raw_documents, y=None):
#         self.fit_transform(raw_documents, y)
#         return self
 
#     def transform(self, raw_documents, copy=True):
#         return self.fit_transform(raw_documents, None)

# from sklearn.pipeline import Pipeline, FeatureUnion
# from sklearn.linear_model import LogisticRegression
# from sklearn.feature_extraction.text import TfidfVectorizer
 
# pipeline_skipthought = Pipeline(steps=[('vectorizer', SkipThoughtsVectorizer()),
#                         ('classifier', LogisticRegression())])
# pipeline_tfidf = Pipeline(steps=[('vectorizer', TfidfVectorizer(ngram_range=(1, 2))),
#                         ('classifier', LogisticRegression())])
 
# feature_union = ('feature_union', FeatureUnion([
#     ('skipthought', SkipThoughtsVectorizer()),
#     ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
# ]))
# pipeline_both = Pipeline(steps=[feature_union,
#                         ('classifier', LogisticRegression())])

# for train_size in (20, 50, 100, 200, 500, 1000, 2000, 3000, len(patents_train)):
#     print(train_size, '--------------------------------------')
#     # skipthought
#     pipeline_skipthought.fit(patents_train[:train_size], classes_train[:train_size])
#     print ('skipthought', pipeline_skipthought.score(tweets_test, classes_test))
 
#     # tfidf
#     pipeline_tfidf.fit(patents_train[:train_size], classes_train[:train_size])
#     print('tfidf', pipeline_tfidf.score(tweets_test, classes_test))
 
#     # both
#     pipeline_both.fit(patents_train[:train_size], classes_train[:train_size])
#     print('skipthought+tfidf', pipeline_both.score(tweets_test, classes_test))
