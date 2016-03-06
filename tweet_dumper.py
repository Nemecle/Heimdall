#!/usr/bin/python
# coding: latin-1
"""
based on https://gist.github.com/yanofsky/5436496

"""

import tweepy
import csv


def get_all_tweets(screen_name):
    """
    get 3200 last tweets of a given @

    """


    tokens = open("Zoehmacarena.tokens", "r")
    consumer_key = tokens.readline()[:-1]
    consumer_secret = tokens.readline()[:-1]
    access_token = tokens.readline()[:-1]
    access_secret = tokens.readline()[:-1]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)


    alltweets = []

    lasttweets = api.user_timeline(screen_name=screen_name, count=200)

    alltweets.extend(lasttweets)


    oldest = alltweets[-1].id - 1


    while len(lasttweets) > 0:
        # print "getting tweets before %s" % (oldest)


        lasttweets = api.user_timeline(screen_name=screen_name, \
            count=200, max_id=oldest)

        alltweets.extend(lasttweets)

        oldest = alltweets[-1].id - 1

        # print "...%s tweets downloaded so far" % (len(alltweets))

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [tweet.text.encode("utf-8") for tweet in alltweets]

    return outtweets




def get_all_tweetsa(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method


    tokens = open("Zoehmacarena.tokens", "r")
    consumer_key = tokens.readline()[:-1]
    consumer_secret = tokens.readline()[:-1]
    access_token = tokens.readline()[:-1]
    access_secret = tokens.readline()[:-1]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    #write the csv
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)

    pass


if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("J_tsar")
