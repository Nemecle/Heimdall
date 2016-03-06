#!/usr/bin/python
# coding: latin-1


class heimdall(object):
    """
    bot manager that start and stop them

    """
    
    def main_loop(self):
        """
        trigger bots and wait for command

        """

        command = ""
        iswatching = True

        for bot in self.bots():
            bot.talk()

        while iswatching:

            command = raw_input("heimdall: ")

            if command[0] is "/": # is a command
                iswatching = False


        return
    
    def add_bot(self, bot):
        """
        add bot to the list of managed bots

        """

        return

    def remove bot(self, name):
        """
        remove bot from the list of managed bots

        """

        returnlist

    def __init__(self):

        self.bots= []
        return



