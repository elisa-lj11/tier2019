# modified from https://gist.github.com/bbengfort/efb311aaa1b52814c284d3b21ae752d6

import nltk
import heapq
import string
import gensim
import itertools

from operator import itemgetter

from nltk import *
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

# new file with weightings
new_file = open("keyphrase_weighting.txt", "w+", encoding="utf-8")

# Corpus variables
CORPUS_TEXT = r'F:\Elisa\text_files'
texts = PlaintextCorpusReader(CORPUS_TEXT, '.*\.txt')

def extract_candidate_chunks(text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):
    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize, POS-tag, and chunk using regular expressions
    chunker = nltk.chunk.regexp.RegexpParser(grammar)
    tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text))
    all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                    for tagged_sent in tagged_sents))
    # join constituent chunk words into a single chunked phrase
    lambda_func = lambda w_p_c: w_p_c[2] != 'O'
    candidates = [' '.join(word for word, pos, chunk in group).lower()
                  for key, group in itertools.groupby(all_chunks, lambda_func) if key]
    return [cand for cand in candidates if cand not in stop_words and not all(char in punct for char in cand)]


def extract_candidate_words(text, good_tags=set(['JJ','JJR','JJS','NN','NNP','NNS','NNPS'])):
	# exclude candidates that are stop words or entirely punctuation
	punct = set(string.punctuation)
	stop_words = set(nltk.corpus.stopwords.words('english'))
	# tokenize and POS-tag words
	tagged_words = itertools.chain.from_iterable(nltk.pos_tag_sents(nltk.word_tokenize(sent)
		for sent in nltk.sent_tokenize(text)))
		# filter on certain POS tags and lowercase all words
	candidates = [word.lower() for word, tag in tagged_words if tag in good_tags and word.lower() not in stop_words and not all(char in punct for char in word)]
	return candidates


def score_keyphrases_by_tfidf(texts, candidates='chunks'):
    # extract candidates from each text in texts, either chunks or words
    extract = {
        'chunks': extract_candidate_chunks,
        'words': extract_candidate_words,
    }[candidates]

    boc_texts = [
        extract(texts.raw(fileid)) for fileid in texts.fileids()
    ]

    # make gensim dictionary and corpus
    dictionary = gensim.corpora.Dictionary(boc_texts)
    corpus = [dictionary.doc2bow(boc_text) for boc_text in boc_texts]

    # transform corpus with tf*idf model
    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    return corpus_tfidf, dictionary


if __name__ == '__main__':
    tfidfs, id2word = score_keyphrases_by_tfidf(texts)
    fileids = texts.fileids()

    # Print top keywords by TF-IDF
    for idx, doc in enumerate(tfidfs):
        new_file.write("Document '{}' key phrases:\n".format(fileids[idx]))
        # Get top 10 terms by TF-IDF score
        for wid, score in heapq.nlargest(100, doc, key=itemgetter(1)):
            new_file.write("{:0.3f}: {}\n".format(score, id2word[wid]))

        new_file.write("\n")