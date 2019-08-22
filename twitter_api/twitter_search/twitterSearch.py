# Created by Elisa Lupin-Jimenez
# modified from https://github.com/ckoepp/TwitterSearch

from TwitterSearch import *
try:

    # CONSTANT: change keywords here to search for different keywords from Twitter
    keywords = [
        "positional audio"
    ]

    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(keywords) # let's define all words we would like to have a look for
    tso.set_language('en') # we want to see German tweets only
    tso.set_include_entities(False) # and don't give us all those entity information
    tso.arguments.update({'tweet_mode': 'extended'})

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        "[redacted]"
    )

    filename = "twitter_search"
    for keyword in keywords:
        filename += "_%s" % keyword
    filename += ".txt"

    print(filename)

    f = open(filename, "w+", encoding="utf-8")

    for tweet in ts.search_tweets_iterable(tso):
        #print(tweet)
        line = '@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['full_text'])
        #print(line)
        #print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
        f.write(line + "\n\n")

    f.close()

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)