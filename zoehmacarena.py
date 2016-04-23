#!/usr/bin/python
# coding: latin-1
"""
file used for small tests. don't mind it

"""

import tweepy
import re
from time import sleep
from tweepy import OAuthHandler

from timeoutdec import timeout, TimeoutError

from markov_test import MarkovInstance


class Zoehmacarena(object):
    """
    Zoeh bot. furnishing this item "as is". I do not provide any
    warranty of the item whatsoever, whether express, implied, or
    statutory, including, but not limited to, any warranty of
    merchantability or fitness for a particular purpose or any
    warranty that its output will make any form of sense.

    """
    def getstatus(self):
        """
        generate status, remove mentions and reduce to 140 characters

        """
        status = "hmmmm je suis à court d'idée. @Nemecle (Error message)"

        status = self.get_rand_tweet("zoepetitchat_tweets.csv")
        status = status.replace('@', '')

        #limit to 140 characters
        status = " ".join(status[:140].split()[:-1])

        return status

    @timeout(5)
    def get_rand_tweet(self, length=100, seed=""):
        """
        try to generate a tweet

        """

        conti = True
        res = []

        while conti:
            text = self.brain.get_rand_string(length, seed)
            if len(text) is not 0:
                text = re.sub(r"(http|https):\/\/[^ ^\n]* ", "", text)
                text = re.sub(r"@", "", text)
                text = re.split(r"[\.\?\!]", text)

                for sentence in text:
                    if len(sentence) > 40 and len(sentence) < 140:
                        conti = False
                        return sentence

    @timeout(5)
    def get_rand_reply(self, length=100, seed=""):
        """
        try to generate a reply

        """

        conti = True
        res = []

        while conti:
            text = self.brain.get_rand_string(length, seed)
            if len(text) is not 0:
                text = re.sub(r"(http|https):\/\/[^ ^\n]* ", "", text)
                text = re.sub(r"@", "", text)
                text = re.split(r"[\.\?\!]", text)

                for sentence in text:
                    if len(sentence) > 40 and len(sentence) < 60:
                        conti = False
                        return sentence


        return -1


    def talk(self):
        """
        talk function for heimdall compatibility

        """
        print(self.get_rand_tweet(100))
        sleep(1)
        return


    def __init__(self, filename, nbrkey, nbrvalue, length):
        """
        create a zoeh instance

        """

        token = open("Zoehmacarena.tokens", "r")
        consumer_key = token.readline()[:-1]
        consumer_secret = token.readline()[:-1]
        access_token = token.readline()[:-1]
        access_secret = token.readline()[:-1]

        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_secret)

        self.api = tweepy.API(self.auth)

        self.brain = Markovinstance(filename, nbrkey, nbrvalue, length)


        lastanswered = ""

        return



def main():
    """
    main loop

    """

    zoeh = Zoehmacarena("zoepetitchat_tweets.csv", 2, 2, 100)


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



    mentions = zoeh.api.mentions_timeline()

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

                answer = zoeh.get_rand_reply()

                print answer

                zoeh.api.update_status("@" + mention.user.screen_name + answer,\
                                  mention.id)



                lastf = open("last.db", "w")
                lastf.write(str(mention.id))
                lastf.close()
            except Exception as exp:
                print "Error while answering: " + str(exp)

            print("\n")

    return

if __name__ == '__main__':
    # main()
    pass

