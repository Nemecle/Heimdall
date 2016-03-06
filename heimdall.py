#!/usr/bin/python
# coding: latin-1

from time import sleep
from multiprocessing import Process, Lock, Pipe, Value

class Heimdall(object):
    """
    bot manager that start and stop them

    """


    def add_bot(self, name, bot, state=-1):
        """
        add bot to the list of managed bots

        """
        statetmp = Value("i", state)
        self.bots.append((name, bot, Value("i", state)))
        return

    def remove_bot(self, name):
        """
        remove bot from the list of managed bots

        """

        for index, (botname, _, _)  in enumerate(self.bots):
            if botname == name:
                self.bots.remove(index)

        return

    def main_loop(self):
        """
        trigger bots and wait for command

        """

        command = ""
        iswatching = True


        print("starting")
        proc.start()
        while cont:
            command = raw_input("Heimdall: ")

            if command == "/quit":
                cont = False
                state.value = -1

            elif command == "/pause":
                l.acquire()
                print("paused")
                ispaused = True

            elif command == "/start":
                print("unpausing")
                l.release()
                ispaused = False

            else:
                print("unknown command")

        proc.join()
        print("finished")
        return

    def __init__(self):

        self.bots= []
        return


def main():

    guardian = Heimdall()
    zoeh = Zoehmacarena()

    guardian.add_bot(zoeh)

    guardian.main_loop()

    cont = True
    ispaused = False
    bobby = Bob()
    state = Value("i", 0)

    l = Lock()
    proc = Process(target=bobby.main, args=(l, state,))

    print("starting")
    proc.start()
    while cont:
        if ispaused:
            command = raw_input("Heimdall[paused]: ")
        else:
            command = raw_input("Heimdall[running]: ")


        if command == "quit":
            cont = False
            state.value = -1

        elif command == "pause":
            l.acquire()
            print("paused")
            ispaused = True

        elif command == "start":
            print("unpausing")
            l.release()
            ispaused = False

        else:
            print("unknown command")

    proc.join()
    print("finished")
    return
