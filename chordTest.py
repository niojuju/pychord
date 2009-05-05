"""
ChordTest :
- Bootstrap Network
- Regular Simulation
- Simulation with Churn
- Simulation with Adversarial Churn
- Un-Bootstrap Network
"""

# IMPORTS
from math import log
from time import sleep
from random import randint 

import sys
import pychord
import chord
import chordViz
from chordLogger import *

# CONSTANTS
# Simulation CONSTANTS
LENGTH_OF_SIMULATION = 10**2
TICK_DELAY = 0.1 # in seconds
# Chord/Network  CONSTANTS
SIZE_OF_NAMESPACE = 2**16 # --> passed into Chord-Network
MAX_NODES = 64      # make 1024 later
MAX_MESSAGES = MAX_NODES/10   # (generated in any tick)
JOIN_LATENCY = 5 # (approximation) how many ticks it takes for a node to completely finish the join process
# Logging  CONSTANTS
VISUALIZE = False # --> passed into Logger
LOG = True
LOG_TO_FILE = False # --> passed into Logger
# Churn CONSTANTS
MAX_CHURN_PERCENT = 2 
MAX_RND_CHURN = MAX_CHURN_PERCENT * MAX_NODES
MAX_ADV_CHURN = log(MAX_NODES, 2) 
CHURN_PDF = 'Uniform' # 'Uniform' or 'PowerLaw'
ADVERSARY = 'Consecutive' # 'Random' or 'Consecutive'
CHURN_PROTECT = 'None' # 'None' or 'Replication' or 'Randomization' -- passed into Chord-Network

def Churn_PRNG(simulation_length):
    if CHURN_PDF is 'Uniform':
        return randint(1, simulation_length)
    if CHURN_PDF is 'PowerLaw':
        CHURN_ALPHA = 2
        return int ( simulation_length * paretovariate(CHURN_ALPHA) )
    
def Tick_All(self):
    tester.tick()
    nw.tick()
    if LOG is True:
        logger.tick()
    if VISUALIZE is True:
        viz.tick()
    
class ChordTest:
   """ simple test. full network, all 16 nodes are there, all routing tables are set """   

   def tick(self):
      # TODO: check if any node's TTL has run out, if has, remove from list
      # assumes that the network will also retire all nodes whose TTL has run out...
   
   def __init__(self):
      self.nodes = []
      self.t = 0
      
if __name__ == "__main__":
   print "## CHORD TESTER ##"
   """ Make class instances """ 
   tester = ChordTest()
   logger = chordLogger()
   #viz = ChordWindow()

   nw = chord.Network(logger)
   
   """ Bootstrap/Initialize network """ 
   # add a fixed number (currently 1) of nodes per tick
   # keep track of nodes that have been added
   # nodes should have random ID (assume no collisions? or check)
   # stop at MAX_NODES * JOIN_LATENCY

   print "\nBootstrapping Network"
   print "---------------------"
   raw_input("Press ENTER to continue... ") # Pause

   nw.bootstrap(3)
   
   # TIME_TO_GROW = JOIN_LATENCY*MAX_NODES
   # for i in range(MAX_NODES):
        # newNodeID = randint(1, SIZE_OF_NAMESPACE-1) # Uniformly at Random
        # # ewNodeTTL = TIME_TO_GROW + Churn_PRNG(LENGTH_OF_SIMULATION)
        # # IME_TO_GROW -= JOIN_LATENCY # all nodes must start TTL countdown at same time
        # newNodeTTL = -1
        # tester.nodes.append((newNodeID, newNodeTTL))
        # nw.add_joins([newNodeID, newNodeTTL]) # add new nodes for the next tick cycle
        # for j in range(JOIN_LATENCY):
            # Tick_All()      

   nw.grow(MAX_NODES)              
                
                   
   """ Normal Simulation (No churn), only messages """
   print "\nNormal Simulation (No churn), only messages"
   print "-------------------------------------------"
   raw_input("Press ENTER to continue... ") # Pause
      
   for i in range(LENGTH_OF_SIMULATION):
       # add new messages
       # tick network
       messages = []
       for j in range( randint(0, MAX_MESSAGES) ): # random no. of messages per tick, but up to MAX_MESSAGES
           srcID =  nw.random_node().id          #tester.nodes[ randint(0, len(tester.nodes)-1) ]
           destID = randint(0, nw.name_space_size-1)  #tester.nodes[ randint(0, len(tester.nodes)-1) ]
           messages.append(chord.Message(srcID, destID))
       nw.add_messages(messages)               
       nw.tick()
       #sleep(TICK_DELAY)
       #print "Tick", i
                   

   print logger.print_state()
   sys.exit(0)
######################################################################
       
       
       
   """ Simulation with random churn """
   # add churn (joins, leaves) upto MAX_RND_CHURN nodes
   # add new messages
   # tick network
   print "\nSimulation with RANDOM churn & messages"
   print "--------------------------------"
   raw_input("Press ENTER to continue... ") # Pause

   for i in range(LENGTH_OF_SIMULATION):       
       #TODO: if there are no nodes in the network currently, skip this
       leaves = []
       for j in range( randint(0, MAX_RND_CHURN) ):
           node_index = randint(0, len(tester.nodes)-1)
           nodeID = tester.nodes.pop( node_index ) # remove from tester.nodes[] immediately
           leaves.append(nodeID) 
       nw.add_leaves(leaves)            

       joins = []
       for j in range( randint(0, MAX_RND_CHURN) ):
           newNodeID = randint(1, SIZE_OF_NAMESPACE-1)
           joins.append(newNodeID) # assumes no collisions as SIZE_OF_NAMESPACE is large
       nw.add_joins(joins)              
              
       #TODO: if there are no nodes in the network currently, skip this
       messages = []
       for j in range( randint(0, MAX_MESSAGES) ):
           srcID = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           destID = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           messages.append(Message(srcID, destID))           
       nw.add_messages(messages)              

       tester.nodes.extend(joins) # add joins[] nodes to tester.nodes lazily
       
       for j in range(JOIN_LATENCY): # assuming same JOIN/LEAVE latency
            nw.tick()
            
       sleep(TICK_DELAY)
              
       
       
   """ Simulation with adversarial churn """
   # sort list of nodes present
   # remove a set of (consecutive) MAX_ADV_CHURN nodes to simulate adversary
   # TODO: add joins too ?     
   # tick network
   print "\nSimulation with ADVERSARIAL churn & messages"
   print "--------------------------------------------"
   raw_input("Press ENTER to continue... ") # Pause

   for i in range(LENGTH_OF_SIMULATION):       
       tester.nodes.sort()
       orginal_ring_size = len(tester.nodes)
       startID = randint(0, orginal_ring_size)
       leaves = []     
       for j in range(0, MAX_ADV_CHURN-1 ):
           node_index = ( startID + j ) % orginal_ring_size
           nodeID = tester.nodes.pop( node_index ) # remove from tester.nodes[] immediately
           leaves.append(nodeID) 
       nw.add_leaves(leaves)               
       
       joins = []
       for j in range( randint(0, MAX_ADV_CHURN) ):
           newNodeID = randint(1, SIZE_OF_NAMESPACE-1)
           joins.append(newNodeID) # assumes no collisions as SIZE_OF_NAMESPACE is large
       nw.add_joins(joins)              
              
       messages = []
       for j in range( randint(0, MAX_MESSAGES) ):
           srcID = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           destID = tester.nodes[ randint(0, len(tester.nodes)-1) ]
           messages.append(Message(srcID, destID))           
       nw.add_messages(messages)              

       tester.nodes.extend(joins) # add joins[] nodes to tester.nodes lazily
       
       for j in range(JOIN_LATENCY): # assuming same JOIN/LEAVE latency
            nw.tick()
            
       sleep(TICK_DELAY)
       
   
   
   
   """ Un-bootstrap network (just for fun) """
   print "\nShutting down network"
   print "---------------------"
   raw_input("Press ENTER to continue... ") # Pause

   # remove a random node from the list
   while len(self.nodes) > 5:
       node_index = randint(0, len(tester.nodes)-1)
       node = tester.nodes.pop( node_index )
       nw.add_leaves([node])
       for j in range(JOIN_LATENCY): # assuming same JOIN/LEAVE latency
            nw.tick()
       sleep(TICK_DELAY)



