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

# A class for each Node / Axis
class wxNode():

    def __init__(self):
        self.linear = True
        self.rotary = False


# A basic class for each Machine
class wxMachine():

    def __init__(self):
        self.axes = []


# Solo/Independent Nodes
# http://pygestalt.org/VMC_IEM.pdf
# p. 35
class wxSolo_Independent():

    def __init__(self):
        pass


# Solo/Gestalt Nodes
# http://pygestalt.org/VMC_IEM.pdf
# p. 36
class wxSolo_Gestalt():

    def __init__(self):
        pass


# Networked/Gestalt Nodes
# http://pygestalt.org/VMC_IEM.pdf
# p. 36
class wxNetworked_Gestalt(wxSolo_Gestalt):

    def __init__(self):
        pass


# Managed/Gestalt Nodes
# http://pygestalt.org/VMC_IEM.pdf
# p. 37
class wxManaged_Gestalt():

    def __init__(self):
        pass


# Compound Nodes
# http://pygestalt.org/VMC_IEM.pdf
# p. 38
class wxCompound_Nodes():

    def __init__(self):
        pass


if __name__ == '__main__':
    pass
