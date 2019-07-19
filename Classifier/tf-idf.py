# adapted from LDA.py
# DOES NOT CURRENTLY WORK
# modifying code from https://gist.github.com/bbengfort/efb311aaa1b52814c284d3b21ae752d6

import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models
import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import heapq
import string
from operator import itemgetter
import os

stemmer = SnowballStemmer('english')

#Readfile and segmentwords taken from cs124, for reading stopword files. 
#Written in python 2 which is why it's weird.
def readFile(fileName):
    contents = []
    f = open(fileName,encoding='utf-8')
    for line in f:
        contents.append(line)
    f.close()
    result = segmentWords('\n'.join(contents)) 
    return result

def segmentWords(s):
    return s.split()

#punctuation = set(readFile('punctuation.txt'))
alphanum = set(['%','#','*','=','.','|','\t'])#,'0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'])

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    text = text.lower()
    text = text.replace('#', ' ')
    text = text.replace('\n',' ')
    text = text.replace('\t',' ')
    for token in gensim.utils.simple_preprocess(text):
       if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
             result.append(lemmatize_stemming(token))
    return result


new_file = open("tf-idf_weighting.txt", "w+", encoding="utf-8")
text_list = []
# CHANGE THIS TO CHANGE SOURCE OF TXT FILES
d = r'F:\Elisa\text_files'

# for path,dirs,files in os.walk(d):
#     for file in files:
#         if not file.endswith('.txt') or file.endswith("handler_list.txt"):
#             continue
#         try:
#             with open(os.path.join(path,file),'r',encoding='utf-8') as f:
#                 text = f.read()
#         except:
#             continue
#         if text == None or text == '':
#             continue
#         text_list.append(text)

# preprocessed_docs = []
# for n,t in enumerate(text_list):
#     # print sample of text before and after processing
#     #if n == (len(text_list) - 1):
#     #    print(("Doc {} (before preproc): {}").format(n, t))
#     #    print(("Doc {}: {}").format(n, p))
#     p = preprocess(t)
#     preprocessed_docs.append(p)

# print("Preprocessed docs len:", len(text_list))

texts = PlaintextCorpusReader(d, ".*\.txt")

boc_texts = [
    extract(texts.raw(fileid)) for fileid in texts.fileids()
]

dictionary = gensim.corpora.Dictionary(boc_texts)
#dictionary = gensim.corpora.Dictionary(preprocessed_docs)
#dictionary.filter_extremes(no_below=10,no_above=.5,keep_n=100000)
#bow_corpus = [dictionary.doc2bow(doc) for doc in preprocessed_docs]
bow_corpus = [dictionary.doc2bow(doc) for boc_text in boc_texts]
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]

fileids = texts.fileids()

for idx, doc in enumerate(corpus_tfidf):
    new_file.write("Document '{}' key phrases:\n".format(fileids[idx]))
    # Get top 100 terms by TF-IDF score
    for wid, score in heapq.nlargest(100, doc, key=itemgetter(1)):
        new_file.write("{:0.3f}: {}\n".format(score, dictionary[wid]))

    new_file.write("\n")


print("Tf-idf weighting has been computed!")
