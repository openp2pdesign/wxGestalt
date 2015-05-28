# -*- coding: utf-8 -*-

#from threading import Thread
import threading


class SimpleThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        # Add here the process
        pass


if __name__ == "__main__":
    pass
