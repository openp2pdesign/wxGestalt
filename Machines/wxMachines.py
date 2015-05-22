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


# Classes

# A class for each Node / Axis
class wxNode(nodes.networkedGestaltNode):

    def __init__(self, axisNumber = 0, axisName = "0 Axis", fabnet = "", persistence = ""):
        self.linear = True
        self.rotary = False
        if self.axisName == "" or self.axisName == "0 Axis":
            self.axisName = str(self.axisNumber)+" Axis"
        self.Node = nodes.networkedGestaltNode(self.axisName, fabnet = fabnet, filename = node_file_path, persistence = persistence)


# Solo/Gestalt Nodes, based on https://github.com/imoyer/gestalt/blob/master/examples/machines/htmaa/single_node.py
# http://pygestalt.org/VMC_IEM.pdf
# p. 36
class wxMachine(machines.virtualMachine):

    def __init__(self, baudRate = 115200, interfaceType = "ftdi", portName = "", nodesNumber = 1):
        self.baudRate = baudRate
        self.interfaceType = interfaceType
        self.portName = portName
        self.nodesNumber = nodesNumber

    def initInterfaces(self):
        if self.providedInterface:
            self.fabnet = self.providedInterface		#providedInterface is defined in the virtualMachine class.
        else:
            self.fabnet = interfaces.gestaltInterface('FABNET', interfaces.serialInterface(baudRate = self.baudRate, interfaceType = self.interfaceType, portName = self.portName))

    def initControllers(self):
        #self.xAxisNode = nodes.networkedGestaltNode('X Axis', self.fabnet, filename = node_file_path, persistence = self.persistence)
        self.xAxisNode = wxNode()
        self.xNode = nodes.compoundNode(self.xAxisNode)

    def initCoordinates(self):
        self.position = state.coordinate(['mm'])

    def initKinematics(self):
        self.xAxis = elements.elementChain.forward([elements.microstep.forward(4), elements.stepper.forward(1.8), elements.leadscrew.forward(6.096), elements.invert.forward(True)])
        self.stageKinematics = kinematics.direct(1)	#direct drive on all axes

    def initFunctions(self):
        self.move = functions.move(virtualMachine = self, virtualNode = self.xNode, axes = [self.xAxis], kinematics = self.stageKinematics, machinePosition = self.position,planner = 'null')
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
