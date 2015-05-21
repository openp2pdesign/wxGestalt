# -*- coding: utf-8 -*-

# Import

# Import for changing the Python Path for importing Gestalt
import sys
import os

# Change the Python Path
base_dir = os.path.dirname(__file__) or '.'
appdir = os.path.abspath(os.path.join(base_dir, os.pardir))
sys.path.insert(0, appdir)

# Import Gestalt
from gestalt import nodes
from gestalt import interfaces
from gestalt import machines
from gestalt import functions
from gestalt.machines import elements
from gestalt.machines import kinematics
from gestalt.machines import state
from gestalt.utilities import notice
from gestalt.publish import rpc	#remote procedure call dispatcher


# Classes

class Axis():

    def __init__(self):
        self.linear = True
        self.rotary = False

class Machine():

    def __init__(self):
        self.axes = []




if __name__ == '__main__':
    pass
