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


FILENAME = "nemecle_tweets.csv"

class Markovinstance(object):
    """
    virtual class intended to be used by bots

    """
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

    def parse_punctuation(self, text):
        """
        replace punctation by keywords

        """

        for char in [", "]:
            text = text.replace(char, " <comma> ")

        for char in ["... ", "… "]:
            text = text.replace(char, " <suspension> ")

        for char in [": ", "; ", ") ", " ("]:
            text = text.replace(char, " <pause> ")

        for char in ["\n", ". ", "! ", "? "]:
            text = text.replace(char, " <stop> ")

        # clean unecessary whitespaces
        ' '.join(text.split())

        return text

    def unparse_punctuation(self, text):
        """
        replace punctation-keywords by punctuation back

        """

        for char in [" <comma> "]:
            text = text.replace(char, ", ")

        for char in [" <suspension> "]:
            text = text.replace(char, "… ")

        for char in [" <stop> ", "<stop> "]:
            text = text.replace(char, random.choice(["\n", ". "," ! ", " ? "]))

        for char in [" <pause> "]:
            text = text.replace(char, random.choice([" : ", " ; "]))

        return text

    def get_rand_string(self, seed="", length=100):
        """
        return a generated string if given length (in word) and
        based on given file

        """

        endstring = ""
        isoutofdata = False
        currentlength = 0

        # seed ?
        if seed is "":
            seed, _ = random.choice(self.wordtuples)

        endstring += str(seed)

        # generate text
        while not isoutofdata and currentlength < length:

            lastwords = " ".join(endstring.split()[-self.nbrkey:])

            possibilities = self.dict_search(lastwords)

            if possibilities is -1 or len(possibilities) is 0:
                endstring += " <stop> "

            else:
                (_, value) = random.choice(possibilities)

                endstring += " " + value

            currentlength = len(endstring.split())

        endstring = self.unparse_punctuation(endstring)


        return endstring


    def talk(self):
        """
        intended as a virtual function.

        """

        print(self.get_rand_string())

        return


    def __init__(self, filename, nbrkey, nbrvalue):

        self.filename = filename
        self.nbrkey = nbrkey
        self.nbrvalue = nbrvalue

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
        for char in ["\""]:
            text = text.replace(char, "")

        text = self.parse_punctuation(text)

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


    bot = Markovinstance(filename, nbrkey, nbrvalue)

    print("15")
    print(bot.get_rand_string(length=15))
    print("20")
    print(bot.get_rand_string(length=20))
    print("25")
    print(bot.get_rand_string(length=25))
    # print("100")
    # print(bot.get_rand_string(length=100))
    # print("1000")
    # print(bot.get_rand_string(length=1000))

    return


if __name__ == '__main__':
    main()
