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
import time
import redis


FILENAME = "nemecle_tweets.csv"

def timeit(method):
    """
    from https://www.andreas-jung.com/contents/a-python-decorator-for-measuring-the-execution-time-of-methods

    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return result

    return timed


class MarkovInstance(object):
    """
    virtual class intended to be used by bots

    """

    def dict_search(self, word):
        """
        search for multiple tuples and return them as a list

        """

        r = redis.Redis("localhost", db=self.dbid)

        # returnlist = []

        # word = str.lower(word)

        # try:
        #     for (key, value) in self.wordtuples:
        #         if bool(re.match(word, key, re.I)):
        #             returnlist.append((key, value))

        # except Exception as exp:
        #     # print "(search) Error while working with dictionary: " + str(exp)\
        #     # + " \nlw: " + lword + " \nword: " + word + " \nkey: " + key
        #     return -1

        return r.lrange(word.lower(), 0, -1)

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

        comma =  [", "]
        suspension = ["… "]
        stop =  [". ", " ! ", " ? "]
        pause = [" : ", " ; "]
    
        x = 0
        while len(re.findall(" <comma> ",  text)) != 0:
            text = re.sub(" <comma> ", random.choice(comma), text, count=1)

        x = 0
        while len(re.findall("( <suspension> |<suspensions>)",  text)) != 0:
            text = re.sub("( <suspension> |<suspension>)", random.choice(suspension), text, count=1)

        x = 0
        while len(re.findall("( <stop> |<stop>)",  text)) != 0:
            text = re.sub("( <stop> |<stop>)", random.choice(stop), text, count=1)

        x = 0
        while len(re.findall("( <pause> |<pause>)",  text)) != 0:
            text = re.sub("( <pause> |<pause>)", random.choice(pause), text, count=1)


            text = text.replace("&lt", "<")
        text = text.replace("&gt", ">")
        text = text.replace(" . ", ". ")

        return text

    @timeit
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
            while any(word in ["<stop>", "<pause>", "<suspensions>", "<comma>"] for word in seed):
                seed, _ = random.choice(self.wordtuples)

        endstring += str(seed)

        # generate text
        while not isoutofdata and currentlength < length:

            lastwords = " ".join(endstring.split()[-self.nbrkey:])

            possibilities = self.dict_search(lastwords)


            if len(possibilities) is 0:
                endstring += " <stop> "
            elif possibilities is -1:
                continue

            else:
                # (_, value) = random.choice(possibilities)
                value = random.choice(possibilities)

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



    def populate_database(self, dbid, filename):
        """
        populate redis database from file

            dbid -- Database ID for isolation
            filename -- textfile to load

            Current databases:
                0. legacy, "zoepetitchat" tag with the whole dictionnary;
                    as  value
                1. zoepetitchat no lowercase database;
                2. zoepetitchat database;
                3. mumbulu databse;
                4. old english long text;
        """

        try:
            with open(filename, 'r') as data:
                text = data.read()
        except Exception as exp:
            print("(main) Error while reading file: " + str(exp))
            return sys.exit(2)

        endstring = ""
        isoutofdata = False
        ite = 0
        r = redis.Redis("localhost", db=dbid)


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

            r.rpush(keywords.lower(), valuewords)
            self.wordtuples.append((keywords, valuewords))



    def __init__(self, dbid, nbrkey, nbrvalue):

        self.nbrkey = nbrkey
        self.nbrvalue = nbrvalue

        self.wordtuples = []
        self.dbid = dbid
        return



def main():
    """
    main loop of the program.

    """
    if len(sys.argv) < 3:
        print("please call the script with one file and two numbers "\
            "as argument.")
        sys.exit(2)

    try:
        dbid = int(sys.argv[1])
        nbrkey = int(sys.argv[2])
        nbrvalue = int(sys.argv[3])
    except Exception:
        print("please call the script with one file and two numbers "\
            "as argument.")
        sys.exit(2)


    bot = MarkovInstance(dbid, nbrkey, nbrvalue)
    # bot.populate_database(0, "zoepetitchat_tweets.csv")

    print(bot.get_rand_string(length=200))
    # print("100")
    # print(bot.get_rand_string(length=100))
    # print("1000")
    # print(bot.get_rand_string(length=1000))

    return


if __name__ == '__main__':
    main()
