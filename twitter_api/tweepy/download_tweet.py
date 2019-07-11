# modified from https://www.allenhuang.org/how-to-download-tweets.html
#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import sys

#Twitter API credentials
"[redacted]"


def get_all_tweets(screen_name):
	print ("getting tweets for %s" % screen_name)
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweet = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	
	searchresult = api.search_users(q='%s' % screen_name)
	
	new_tweets = ''
	exist = 0
	for temp in searchresult:
		if temp.screen_name == screen_name:
			new_tweets = api.user_timeline(screen_name = screen_name,count=200)
			exist = 1
	if exist == 0:
		print ("Twitter name does not exist! Please check!")
	
	#save most recent tweets
	alltweet.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	if alltweet:
		oldest = alltweet[-1].id - 1
	elif exist == 1:
		print ("Twitter name correct but no tweet at all!")
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ("    getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweet.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweet[-1].id - 1
		
		print ("    ...%s tweets downloaded so far" % (len(alltweet)))

	is_retweet = [];
	for tweet in alltweet:
		if hasattr(tweet, 'retweeted_status') == True:
			is_retweet.append("1")
		else:
			is_retweet.append("0")


	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweet]

	#write the csv	
	with open('%s.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["tweet_id","tweet_time","tweet"])
		writer.writerows(outtweets)
	pass
	with open('%s_retweet.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["is_retweet"])
		writer.writerows(is_retweet)
	pass

if __name__ == '__main__':
	#pass in the username of the account you want to download
	#get_all_tweets("tim_cook")
	#get_all_tweets(sys.argv[1])
	#var = input("Input the twitter handler you want to download: ")
	#get_all_tweets(var)

	with open('handler_list.txt') as list:
		handlerlist = csv.reader(list)
		for handler in handlerlist:
			get_all_tweets(handler[0])
	pass

	