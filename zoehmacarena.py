#!/usr/bin/python
# coding: latin-1
"""
file used for small tests. don't mind it

"""

import tweepy
from time import sleep
from tweepy import OAuthHandler

import markov_test as mt

def getstatus():
    """
    generate status, remove mentions and reduce to 140 characters

    """
    status = "hmmmm je suis à court d'idée. @Nemecle (Error message)"

    status = mt.get_rand_tweet("zoepetitchat_tweets.csv", 20, 2, 1)
    status = status.replace('@', '')

    #limit to 140 characters
    status = " ".join(status[:140].split()[:-1])

    return status

def bot_invasion():
    """
    bot that tweets

    """

    #authorize twitter, initialize tweepy
    token = open("Zoehmacarena.tokens", "r")

    consumer_key = token.readline()[:-1]
    consumer_secret = token.readline()[:-1]
    access_token = token.readline()[:-1]
    access_secret = token.readline()[:-1]

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    for nbr in range(1000):
        status = getstatus()
        api.update_status(status)
        print "I tweeted \"" + status + "\""
        sleep(62)


    return

def random_tweet():
    """
    tweet once.

    """

    conti = True
    while conti:
        text = mt.get_rand_tweet("zoepetitchat_tweets.csv")
        if len(text) is not 0:
            conti = False
            return text

    return -1

def main():
    """
    main loop

    """

    token = open("Zoehmacarena.tokens", "r")
    consumer_key = token.readline()[:-1]
    consumer_secret = token.readline()[:-1]
    access_token = token.readline()[:-1]
    access_secret = token.readline()[:-1]

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)


    lastanswered = ""

    try:
        lastf = open("last.db", "r")
        lastanswered = int(lastf.readline())
        lastf.close()
    except:
        lastanswered = ""


    # if lastanswered is not "":
    #     mentions = api.mentions_timeline(since_id=lastanswered)

    # else:
    #     mentions = api.mentions_timeline()



    mentions = api.mentions_timeline()

    for mention in reversed(mentions):
        print str(mention.id)
        print mention.user.screen_name
        print mention.text + "\n\n"

    for mention in reversed(mentions):
        # print mention.id
        # print mention.user.screen_name
        # print mention.text

        if str(mention.id) is "698147667990441984":
            print "found"
            try:

                answer = mt.get_rand_reply("zoepetitchat_tweets.csv", length=400)

                print answer

                api.update_status("@" + mention.user.screen_name + answer,\
                                  mention.id)



                lastf = open("last.db", "w")
                lastf.write(str(mention.id))
                lastf.close()
            except Exception as exp:
                print "Error while answering: " + str(exp)

            print("\n")

    return

if __name__ == '__main__':
    main()

