#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
markov chain experimentation

call by giving a original set of word to start with (more than nbrkey)

The program cut the given text by word, based on space
It takes a certain number (nbrkey) of following words, for instance two
by two, and associate to this tuple another sequence of word of length
nbrvalue
finally it create a dictionary based on these associations and chain
them to generate the text

I personally populate "text_data.txt" with http://norvig.com/big.txt

Also try to use https://gist.github.com/yanofsky/5436496
"""

import sys
import random
import re
from timeoutdec import timeout, TimeoutError


FILENAME = "nemecle_tweets.csv"

class Markov_instance(object):
    def dict_search(self, word):
        """
        search for multiple tuples and return them as a list
    
        """
    
        returnlist = []
    
        lword = str.lower(word)
    
        try:
            for (key, value) in self.wordtuples:
                if bool(re.match(word, key, re.I)):
                    returnlist.append((key, value))
    
        except Exception as exp:
            # print "(search) Error while working with dictionary: " + str(exp)\
            # + " \nlw: " + lword + " \nword: " + word + " \nkey: " + key
            return -1
    
        return returnlist

    def get_rand_string(self, seed="", length=100):
        """
        return a generated string if given length (in word) and
        based on given file
    
        """

        endstring = ""
        isoutofdata = False
        ite = 0
        # print("starting with seed")
        if seed is "":
            seed, _ = random.choice(self.wordtuples)
    
        endstring += seed
    
        # print("starting adding samples")
        while not isoutofdata and ite < self.length:
            lastword = " ".join(endstring.split()[-self.nbrkey:])
            possibilities = self.dict_search(lastword)
            if possibilities is -1:
                isoutofdata = True
            elif len(possibilities) is 0:
                isoutofdata = True
            else:
                (key, value) = random.choice(possibilities)
    
                endstring += " " + value
    
                ite += 1
            
        for char in [" . " ," , ", " ... "]:
            endstring = endstring.replace(char, char.replace(" ", "") + " ") 
        for char in [" : ", " ; ", " ? ", " ! "]:
            endstring = endstring.replace(char, " " + char.replace(" ", "") + " ") 
        
        
        return endstring

    @timeout(5)
    def get_rand_tweet(self, datafile, length=100, nbrkey=3, nbrvalue=1, seed=""):
    
        conti = True
        res = []
    
        while conti:
            text = get_rand_string(length, seed)
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
    
        conti = True
        res = []
    
        while conti:
            text = get_rand_string(length, seed)
            if len(text) is not 0:
                text = re.sub(r"(http|https):\/\/[^ ^\n]* ", "", text)
                text = re.sub(r"@", "", text)
                text = re.split(r"[\.\?\!]", text)
    
                for sentence in text:
                    if len(sentence) > 40 and len(sentence) < 60:
                        conti = False
                        return sentence
    
    
        return -1


    def __init__(self, filename, nbrkey, nbrvalue, length):
        
        self.filename = filename
        self.nbrkey = nbrkey
        self.nbrvalue = nbrvalue
        self.length = length

        self.wordtuples = []

        
        try:
            with open(filename, 'r') as data:
                text = data.read()
        except Exception as exp:
            print("(main) Error while reading file: " + str(exp))
            return sys.exit(2)
    
        endstring = ""
        isoutofdata = False
        ite = 0
    
        # print("striping unwanted characters")
        for char in ["\"", ")", "(", "]", "[", "=", "\n"]:
            text = text.replace(char, "")


        # to process punctation right
        for char in [". ",", ", " : ", " ; ", "... ", " ! ", " ? "]:
            text = text.replace(char, " " + char)

        text = text.split()
        self.numberofword = len(text)
    
    
        # feeding data
        # print("creating tuples")
        for nbr in range(0, self.numberofword - self.nbrkey - self.nbrvalue):
            keywords = []
            valuewords = []
            for key in range(nbr, nbr + self.nbrkey):
                keywords.append(text[key])
            for key in range(nbr + self.nbrkey, nbr + self.nbrkey + self.nbrvalue):
                valuewords.append(text[key])
    
    
            keywords = ''.join(str(e) + " " for e in keywords)
            keywords = " ".join(keywords.split())
    
            valuewords = ''.join(str(e) + " " for e in valuewords)
            valuewords = " ".join(valuewords.split())
    
            # print "\"" + keywords + "\" \"" + valuewords + "\""
    
            self.wordtuples.append((keywords, valuewords))
    
            # print(str(nbr) + " tuples created")

        return



def main():
    """
    main loop of the program.

    """

    length = 100
    if len(sys.argv) < 3:
        print("please call the script with one file and two numbers "\
            "as argument.")
        sys.exit(2)

    try:
        filename = sys.argv[1]
        nbrkey = int(sys.argv[2])
        nbrvalue = int(sys.argv[3])
    except Exception:
        print("please call the script with one file and two numbers "\
            "as argument.")
        sys.exit(2)

    try:
        #3rd argument is optional
        length = int(sys.argv[4])
    except Exception:
        pass

    bot =Markov_instance(filename, nbrkey, nbrvalue, length)

    print bot.get_rand_string()
    print bot.get_rand_string()
    print bot.get_rand_string()
    print bot.get_rand_string()
    print bot.get_rand_string()

    return


if __name__ == '__main__':
    main()
