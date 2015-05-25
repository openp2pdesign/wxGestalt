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

    def __init__(self, axisNumber = 0, fabnet = "", persistence = ""):
        self.linear = True
        self.rotary = False
        self.axisNumber = int(axisNumber)
        self.axisName = "Node #",str(axisNumber+1)
        self.Node = nodes.networkedGestaltNode(self.axisName, fabnet = fabnet, filename = node_file_path, persistence = persistence)


# Basic machines made of n gestalt nodes
class wxMachine(machines.virtualMachine):

    def __init__(self, baudRate = baudratesList[16], interfaceType = "ftdi", portName = "", nodesNumber = 0):
        self.baudRate = baudRate
        self.interfaceType = interfaceType
        self.portName = portName
        self.nodesNumber = int(nodesNumber)
        self.machineNodes = {}
        self.machineAxes = {}
        self.machineAxesNode = {}

    def initInterfaces(self):
        if self.providedInterface:
            self.fabnet = self.providedInterface		#providedInterface is defined in the virtualMachine class.
        else:
            self.fabnet = interfaces.gestaltInterface('FABNET', interfaces.serialInterface(baudRate = self.baudRate, interfaceType = self.interfaceType, portName = self.portName))

    def initControllers(self):
        for each_node in range(self.nodesNumber):
            self.machineAxesNodes[each_node] = wxMachineNodes(axisNumber = each, fabnet = self.fabnet, persistence = self.persistence )
        self.machineNodes = nodes.compoundNode(self.machineAxesNodes.values())

    def initCoordinates(self):
        measure_units = []
        for each_node in range(self.nodesNumber):
            measure_units.append('mm')
        self.position = state.coordinate(measure_units)

    def initKinematics(self):
        for each_node in range(self.nodesNumber):
            self.machineAxes[each_node] = elements.elementChain.forward([elements.microstep.forward(4), elements.stepper.forward(1.8), elements.leadscrew.forward(6.096), elements.invert.forward(True)])
        self.stageKinematics = kinematics.direct(self.nodesNumber)	#direct drive on all axes

    def initFunctions(self):
        self.move = functions.move(virtualMachine = self, virtualNode = self.machineNodes, axes = [self.machineAxes.values()], kinematics = self.stageKinematics, machinePosition = self.position,planner = 'null')
        self.jog = functions.jog(self.move)	#an incremental wrapper for the move function

    def initLast(self):
        #self.machineControl.setMotorCurrents(aCurrent = 0.8, bCurrent = 0.8, cCurrent = 0.8)
        #self.xyzNode.setVelocityRequest(0)	#clear velocity on nodes. Eventually this will be put in the motion planner on initialization to match state.
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


if __name__ == '__main__':
    pass
