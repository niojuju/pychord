"""
ChordTest :
- Bootstrap Network
- Regular Simulation
- Simulation with Churn
- Un-Bootstrap Network
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
MAX_RND_CHURN = MAX_CHURN_PERCENT * MAX_NODES
CHURN_PDF = ['Uniform', 'Poisson']


class ChordTest:
   """ simple test. full network, all 16 nodes are there, all routing tables are set """   

   def __init__(self):
      self.nodes = []
      self.t = 0
      
if __name__ == "__main__":
   """ Make class instances """ 
   tester = ChordTest()
   logger = chordLogger()
   nw = pychord.Network(SIZE_OF_NAMESPACE) # should be SIZE_OF_NAMESPACE

   """ Bootstrap/Initialize network """ 
   # add a fixed number (currently 1) of nodes per tick
   # keep track of nodes that have been added
   # nodes should have random ID (assume no collisions? or check)
   # stop at MAX_NODES * JOIN_LATENCY

   print "Bootstrapping Network"
   print "---------------------"
   
   for i in range(MAX_NODES*0.9):
        newNodeID = randint(1,SIZE_OF_NAMESPACE-1)
        tester.nodes.append(newNodeID)
        nw.add_joins([newNodeID]) # add new nodes for the next tick cycle
        for j in range(JOIN_LATENCY):
            nw.tick()                    

   # Pause         
   raw_input("Press ENTER to continue... ")
                
                
                
   """ Normal Simulation (No churn), only messages """
   print "Normal Simulation (No churn), only messages"
   print "-------------------------------------------"
      
   for i in range(LENGTH_OF_SIMULATION):
       # add new messages
       # tick network
       messages = []
       for j in range( randint(0, MAX_MESSAGES) ): # random no. of messages per tick, but up to MAX_MESSAGES
           srcID = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           destID = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           messages.append(Message(srcID, destID))
       nw.add_messages(messages)               
       nw.tick()
       sleep(0.1)
       #print "Tick", i
             
   # Pause         
   raw_input("Press ENTER to continue... ")
      
 
       
       
       
   """ Simulation with random churn """
   # add new messages
   # add churn (joins, leaves) upto MAX_RND_CHURN nodes
   # tick network
   print "Simulation with RANDOM churn & messages"
   print "--------------------------------"

   for i in range(LENGTH_OF_SIMULATION):
       # add new messages
       # tick network
       messages = []
       for j in range( randint(0, MAX_MESSAGES) ):
           srcID = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           destID = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           messages.append(Message(srcID, destID))           
       nw.add_messages(messages)              
       
       joins = []
       for j in range( randint(0, MAX_RND_CHURN) ):
           nodeID = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           joins.append(nodeID)
       nw.add_joins(joins)              
       
       leaves = []
       for j in range( randint(0, MAX_RND_CHURN) ):
           node_index = randint(0, len(tester.nodes)-1)
           nodeID = tester.nodes.pop( node_index )
           leaves.append(nodeID) 
       nw.add_leaves(leaves)              

       tester.nodes.append(nodeID) # add nodes in joins[] after getting leaves[]
       
       for j in range(JOIN_LATENCY): # assuming same JOIN/LEAVE latency
            nw.tick()
            
       sleep(0.1)
       
   # Pause         
   raw_input("Press ENTER to continue... ")
   
       
       
       
   """ Simulation with adversarial churn """
   # sort list of nodes present
   # remove conseq. MAX_ADV_CHURN nodes to simulate adversary
   # TODO: add joins too ?     
   # tick network
   print "Simulation with ADVERSARIAL churn & messages"
   print "--------------------------------------------"

   for i in range(LENGTH_OF_SIMULATION):
       # add new messages
       # tick network
       messages = []
       for j in range( randint(0, MAX_MESSAGES) ):
           srcID = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           destID = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           messages.append(Message(srcID, destID))           
       nw.add_messages(messages)              
       
       joins = []
       for j in range( randint(0, MAX_RND_CHURN) ):
           nodeID = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           joins.append(nodeID)
       nw.add_joins(joins)              
       
       leaves = []
       for j in range( randint(0, MAX_RND_CHURN) ):
           node_index = randint(0, len(tester.nodes)-1)
           nodeID = tester.nodes.pop( node_index )
           leaves.append(nodeID) 
       nw.add_leaves(leaves)              

       tester.nodes.append(nodeID) # add nodes in joins[] after getting leaves[]
       
       for j in range(JOIN_LATENCY): # assuming same JOIN/LEAVE latency
            nw.tick()
            
       sleep(0.1)
   
   # Pause         
   raw_input("Press ENTER to continue... ")
   
   
   
   """ Un-bootstrap network (just for fun) """
   print "Shutting down network"
   print "---------------------"

   # remove a random node from the list
   while len(self.nodes) > 5:
       node_index = randint(0, len(tester.nodes)-1)
       node = tester.nodes.pop( node_index )
       nw.add_leaves([node])
       for j in range(JOIN_LATENCY): # assuming same JOIN/LEAVE latency
            nw.tick()
    sleep(0.1)
