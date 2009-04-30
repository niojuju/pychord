"""
Constants:
- SIZE_OF_NAMESPACE = 2^16 ??
- MAX_NODES = 2^10 = 1024 currently
- MAX_CHURN_PERCENT = 2 
- VISUALIZE = true
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
import pychord
import chordViz
import chordLogger


# CONSTANTS
VISUALIZE = true
SIZE_OF_NAMESPACE = 2**16
MAX_NODES = 64      # make 1024 later
MAX_CHURN_PERCENT = 2 
MAX_MESSAGES  = (1/100) * MAX_NODES    # (generated in any tick)
CHURN_PDF = ['Uniform', 'Poisson', 'Weibull']


class ChordTest:
   """ simple test. full network, all 16 nodes are there, all routing tables are set """   

   def __init__(self):
      self.nodes = []
      self.t = 0

      #init nodes
      for i in range(SIZE):
         self.nodes.append(Node(i))
      
      #init routing tables
      
      for i in range(SIZE):
         self.nodes[i].fingers = []
         #print log(SIZE,2), "links"
         for j in range(log(SIZE,2)):
            #print "link to :", (i+(2**j))%SIZE, i, j
            self.nodes[i].fingers.append(self.nodes[(i+(2**j))%SIZE])



      #test messages
      from random import randint 
      #send_message(self.nodes[1], Message(randint(1,SIZE-1),randint(1,SIZE-1),i)) #random message
      send_message(self.nodes[1], Message(1,52,1)) #random message
      send_message(self.nodes[1], Message(45,12,5)) #random message
      

   def tick(self):
      self.t += 1
     # print "tick", self.t
      for n in self.nodes:
         n.tick(self.t)



if __name__ == "__main__":
   test = ChordTest()
   test.tick()
   test.tick()
   test.tick()
   test.tick()
   test.tick()
   test.tick()
   test.tick()

