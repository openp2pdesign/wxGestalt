# -*- coding: utf-8 -*-

import time
import wx

from threading import Thread

class SimpleThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        # Add here the process
        pass

    def stop(self):
        self.stopped = True


if __name__ == "__main__":
    pass
