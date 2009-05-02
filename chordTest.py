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
LENGTH_OF_SIMULATION = 10**2

# Chord/Network  CONSTANTS
SIZE_OF_NAMESPACE = 2**16
MAX_NODES = 64      # make 1024 later
MAX_MESSAGES = MAX_NODES/10   # (generated in any tick)

JOIN_LATENCY = 5 # takes JOIN_LATENCY ticks for a node to completely finish the join process


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
        #send_message(self.nodes[1], Message(randint(1,SIZE-1),randint(1,SIZE-1),i)) #random message
        send_message(self.nodes[1], Message(1,52,1)) #random message
        send_message(self.nodes[1], Message(45,12,5)) #random message
        return

if __name__ == "__main__":
   """ Make class instances """ 
   tester = ChordTest()
   # logger = chordLogger()
   nw = pychord.Network(SIZE_OF_NAMESPACE) # should be SIZE_OF_NAMESPACE

   """ Bootstrap/Initialize network """ 
   # add a fixed number (currently 1) of nodes per tick
   # keep track of nodes that have been added
   # nodes should have random ID (assume no collisions? or check)
   # stop at MAX_NODES * JOIN_LATENCY

   print "Bootstrapping Network"
   print "---------------------"
   
   for i in range(MAX_NODES*0.9):
        newnode = randint(1,SIZE_OF_NAMESPACE-1)
        tester.nodes.append(newnode)
        nw.add_joins([newnode]) # add new nodes for the next tick cycle
        # TODO: Ask Tom to change interface for add_joins to accept only IDs (not node objects)
        for j in range(JOIN_LATENCY):
            nw.tick()                    
   
   """ Normal Simulation (No churn), only messages """
   print "Normal Simulation (No churn), only messages"
   print "-------------------------------------------"
    
   
   for i in range(LENGTH_OF_SIMULATION):
       # add new messages
       # tick network
       messages = []
       for j in range( randint(0, MAX_MESSAGES) ):
           src = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           dest = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           messages.append(Message(src, dest))
       nw.add_messages(messages)               
       nw.tick()
       sleep(0.1)
       #print "Tick", i
             
   """ Simulation with random churn """
  # add new messages
  # add churn (joins, leaves) upto MAX_RND_CHURN nodes
  # tick network

   for i in range(LENGTH_OF_SIMULATION):
       # add new messages
       # tick network
       messages = []
       for j in range( randint(0, MAX_MESSAGES) ):
           src = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           dest = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           messages.append(Message(src, dest))           
       nw.add_messages(messages)              
       
       joins = []
       for j in range( randint(0, MAX_CHURN_PERCENT * MAX_NODES) ):
           node = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           joins.append(node)           
       nw.add_joins(joins)              
       
       leaves = []
       for j in range( randint(0, MAX_CHURN_PERCENT * MAX_NODES) ):
           node = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           tester
           joins.append(node)           
       nw.add_leaves(leaves)              
        
       for j in range(JOIN_LATENCY): # assuming same JOIN/LEAVE latency
            nw.tick()
            
       sleep(0.1)
       
       
   
   """ Simulation with adversarial churn """
       # sort list of nodes present
       # remove conseq. MAX_ADV_CHURN nodes to simulate adversary
   
   """ Un-bootstrap network (just for fun) """
       # remove a random node from the list
