# -*- coding: utf-8 -*-

# Import

# Import for changing the Python Path for importing Gestalt
import sys
import os
# Import sleep
from time import sleep

# Change the Python Path if needed
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
from gestalt.publish import rpc    #remote procedure call dispatcher


# Variables

# This is needed for loading the 086-005a.py file from the Gestalt folder
node_file_path = "gestalt/examples/machines/htmaa/086-005a.py"

# Baudrates
baudratesList = [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000]
baudratesListStrings = [str(i) for i in baudratesList]
# interfaces
interfacesList = ['ftdi','lufa','genericSerial']


# Classes

# A class for each Node / Axis
class wxMachineNodes():

    def __init__(self, axisNumber = 0, interface = None, persistenceFile = "wxGestalt.vmp",*args, **kw):
        self.linear = True
        self.rotary = False
        self.axisNumber = int(axisNumber)
        self.axisName = "Node #"+str(axisNumber+1)
        self.name = self.axisName
        self.interface = interface
        self.Node = nodes.networkedGestaltNode(name = self.axisName, interface = self.interface, persistenceFile = persistenceFile, filename = "gestalt/examples/machines/htmaa/086-005a.py")


# Basic machines made of n gestalt nodes for the GUI
class wxMachineGUI():

    def __init__(self, nodesNumber = 0):
        self.nodesGUI = {}
        self.nodesNumber = nodesNumber
        self.initNodesGUI(self.nodesNumber)

    def initNodesGUI(self, number):
        for each_node in range(number):
            self.nodesGUI[each_node] = {}
            self.nodesGUI[each_node]["linear"] = True
            self.nodesGUI[each_node]["rotary"] = False


# Basic machines made of n gestalt nodes
class wxMachine(machines.virtualMachine):

    def __init__(self, baudRate = baudratesList[16], interface = None, interfaceType = "ftdi", portName = "", nodesNumber = 0, persistenceFile = "wxGestalt.vmp", *args, **kw):
        self.persistenceFile = persistenceFile
        self.baudRate = baudRate
        self.providedInterface = interface
        self.interfaceType = interfaceType
        self.portName = portName
        self.nodesNumber = int(nodesNumber)
        self.machineNodes = {}
        self.machineAxes = {}
        self.machineAxesNodes = {}
        self.providedInterface = interface
        self.publishEnabled = True

    def initMachine(self):
        # self.initInterfaces()
        # self.initControllers()
        # self.initCoordinates()
        # self.initKinematics()
        # self.initFunctions()

        self.initInterfaces()
        self.initControllers()
        self.initCoordinates()
        self.initKinematics()
        self.initFunctions()
        self.initPublish()
        self.initLast()
        self.publish()

    def initInterfaces(self):
        if self.providedInterface:
            self.fabnet = self.providedInterface        #providedInterface is defined in the virtualMachine class.
        else:
            self.fabnet = interfaces.gestaltInterface('FABNET', interfaces.serialInterface(baudRate = self.baudRate, interfaceType = self.interfaceType, portName = self.portName))

    def initControllers(self):
        for each_node in range(self.nodesNumber):
            temp = wxMachineNodes(axisNumber = each_node, interface = self.fabnet, persistenceFile = self.persistenceFile)
            self.machineAxesNodes[each_node] = temp.Node
        toCompound = (node for node in self.machineAxesNodes.values())
        self.machineNodes = nodes.compoundNode(*toCompound)

    def initCoordinates(self):
        measure_units = []
        for each_node in range(self.nodesNumber):
            measure_units.append('mm')
        self.position = state.coordinate(measure_units)

    def initKinematics(self):
        for each_node in range(self.nodesNumber):
            self.machineAxes[each_node] = elements.elementChain.forward([elements.microstep.forward(4), elements.stepper.forward(1.8), elements.leadscrew.forward(6.096), elements.invert.forward(True)])
        self.stageKinematics = kinematics.direct(self.nodesNumber)    #direct drive on all axes

    def initFunctions(self):
        self.move = functions.move(virtualMachine = self, virtualNode = self.machineNodes, axes = self.machineAxes.values(), kinematics = self.stageKinematics, machinePosition = self.position,planner = 'null')
        self.jog = functions.jog(self.move)    #an incremental wrapper for the move function

    def initLast(self):
        #self.machineControl.setMotorCurrents(aCurrent = 0.8, bCurrent = 0.8, cCurrent = 0.8)
        #self.xyzNode.setVelocityRequest(0)    #clear velocity on nodes. Eventually this will be put in the motion planner on initialization to match state.
        pass

    def publish(self):
        #self.publisher.addNodes(self.machineControl)
        pass

    def getPosition(self):
        return {'position':self.position.future()}

    def setPosition(self, position  = [None]):
        self.position.future.set(position)

    def setSpindleSpeed(self, speedFraction):
        #self.machineControl.pwmRequest(speedFraction)
        pass

    def testMachine(self):
        # Test node
        number = self.nodesNumber
        print "Number of nodes:",number
        if number == 1:
            moves = [[10],[20],[10],[0]]
        elif number == 2:
            moves = [[10,10],[20,20],[10,10],[0,0]]
        elif number == 3:
            moves = [[10,10,10],[20,20,20],[10,10,10],[0,0,0]]
        elif number == 4:
            moves = [[10,10,10,10],[20,20,20,20],[10,10,10,10],[0,0,0,0]]

        print
        print "Testing the nodes..."
        # Send the test coordinates to the move function
        self.moveMachine(moves)

    def moveMachine(self,moves):
        # Set velocity
        self.machineNodes.setVelocityRequest(8)

        # Launch coordinates
        for coords in moves:
            self.move(coords, 0)
            status = self.machineNodes.spinStatusRequest()
            while status[0]['stepsRemaining'] > 0:
                  sleep(0.001)
                  status = self.machineNodes.spinStatusRequest()

        print
        print "Nodes tested successfully."


if __name__ == '__main__':
    pass
