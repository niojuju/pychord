"""
Constants:
- SIZE_OF_NAMESPACE = 2^16 ??
- MAX_NODES = 2^10 = 1024 currently
- MAX_CHURN_PERCENT = 2 
- VISUALIZE
- LOG_TO_FILE
- MAX_MESSAGES (generated in any tick) = 1% x MAX_NODES
- CHURN_PDF = {Uniform, Poisson, Weibull}

Methods: 
- None, only __main__

Bootstrap Network:
- Init
- generate joins [with random id] (1 per tick?)
- call tick on n/w & ( viz OR Logger ?)

Regular Simulation:
- generate [a random no. of] messages per tick from a [random] node to a [random] node
- call tick on n/w & ( viz OR Logger ?)

Simulation with Churn:
- generate [a random no. of] messages per tick from a [random] node to a [random] node
- generate [a random no. of] churn per tick
- call tick on n/w & ( viz OR Logger ?)

"""

# IMPORTS
from math import log
from time import sleep
from random import randint 

import pychord
import chordViz
import chordLogger


# Simulation CONSTANTS
TICKS_DURATION = 2**5

# Chord/Network  CONSTANTS
SIZE_OF_NAMESPACE = 2**16
MAX_NODES = 64      # make 1024 later
MAX_MESSAGES = MAX_NODES/10   # (generated in any tick)

# Logging  CONSTANTS
VISUALIZE = True
LOG_TO_FILE = True

# Churn CONSTANTS
MAX_CHURN_PERCENT = 2 
CHURN_PDF = ['Uniform', 'Poisson', 'Weibull']


class ChordTest:
   """ simple test. full network, all 16 nodes are there, all routing tables are set """   

   def __init__(self):
      self.nodes = []
      self.t = 0


   def add_new_messages(nw):
        #test messages
        from random import randint 
        #send_message(self.nodes[1], Message(randint(1,SIZE-1),randint(1,SIZE-1),i)) #random message
        send_message(self.nodes[1], Message(1,52,1)) #random message
        send_message(self.nodes[1], Message(45,12,5)) #random message
        return

if __name__ == "__main__":
   """ Make class instances """ 
   # tester = ChordTest()
   # logger = chordLogger()
   nw = pychord.Network(MAX_NODES) # should be SIZE_OF_NAMESPACE

   """ Bootstrap/Initialize network """ 
   # add a fixed number of nodes per tick
   # keep track of nodes that have been added
   # nodes should have random ID (assume no collisions? or check)
   # stop at MAX_NODES * JOIN_DURATION
   
   """ Normal Simulation (No churn) """
   for i in range(10):
       print "Tick", i
       # add new messages
       # tick network
       nw.tick()
       sleep(0.1)
       
   """ Simulation with random churn """
       # add new messages
       # add churn (joins, leaves)
       # tick network
   
   """ Simulation with adversarial churn """
   
   """ Un-bootstrap network (just for fun) """
       # remove a random node from the list
