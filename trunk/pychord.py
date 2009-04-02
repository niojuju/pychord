from math import log
# maximum size of teh chord network / size fo the address space
SIZE = 1024


#a global dictionary to hold the messages that are to be processed by teh nodes at this timestep
#key = node this event is to be handled by
#val = a list of events. each event is some sort of event description that is interpreted by teh node 
#at each timestep the nodes will handle teh messages from teh last round and create new events for teh next round
chord_messages = {}




# simple helper function.  returns true if x lies between i and j on the adress space ring
def between(x, i, j):
   if i <= j:
      return x >= i and x <=j
   else: #this spans the origin
      return x >= i or x<= j






#A simple class to hold some data representing a message on teh network
class Message:

   def __init__(self, src, dest, time_stamp, transfer_time=3, content=""):
      self.dest = dest
      self.src = src
      self.init_time =time_stamp
      self.t =time_stamp
      self.content = content
      self.current_location = src
      self.last_location = src
      self.num_hops = 0
      self.transfer_time = transfer_time



   def __str__(self):
      return "<Message, from:%d, to:%d, t:%d(%d), contents:%s>from:%s" % (self.src, self.dest, self.t,self.init_time, self.content, self.last_location) 



#sends msg to node
#puts the message into the global chord_messages array so that teh receivingnode will handle it during the next step
def send_message(node, msg):
   global chord_messages

   try:
      node = node.id
   except: #its an int, so were good
      pass 

   if node in chord_messages:
      chord_messages[node].append(msg)
   else:
      chord_messages[node] = [msg] # create a new list teh first time this node gets a mesage


#A node in the Chord network
class Node:

   def __init__(self, id):
      self.id = id
      self.fingers = []
      self.predecessor = None
      self.time = 0
      

      #the pending list will hold info so that we can remember what requests we are still waiting for
      #when we initialize a search or join well add areminder here until we receuive ananswer
      #we will always puta  timestamp with each request when we put it in here so that we can knwo 
      #when to stop waiting/label teh request failed by  exceeded TTL
      self.pending = [] 



   #is called at each time step during teh simulation, teh node is allowed to handle its incoming messages
   #dt = current time step
   #whats best for simualtion here?  only one event per timestep?  
   #all taht are enqueud at timesteop but not what other dop during this timestep?
   #possibly approximate network delay by setting dt of new events to next round + delay
   def tick(self, dt):
      global chord_messages
      self.time = dt
      if not self.id in chord_messages:
         return #nothing to be done

      messages = chord_messages[self.id]
      consumed = []

      for i  in range(len(messages)):
         msg = messages[i]

         if msg.content == "OK":  #this one is an established link...keep it alive until data transfer is done
            if dt-msg.t > msg.transfer_time: consumed.append(msg)
            continue

         if msg.t < self.time: #dont handle events that were added this round
            if self.find_successor(msg): #returns value only if dest (successor) is reached
               print "Home:", self, msg
            consumed.append(msg)

      for m in consumed:
         messages.remove(m)


   #tries to route the message / find teh successor of msg.dest            
   def find_successor(self, msg):
   
      if between(msg.dest, self.id, self.fingers[0].id) and msg.dest < self.fingers[0].id:
         #respond
         msg.content = "OK"
         send_message(msg.src, msg)
         msg.last_location = msg.current_location
         msg.current_location = msg.src         
         return self.fingers[0].id
      
      #route to next closest
      node = self.closest_preceding_node(msg)
      msg.t = self.time 
      print "routing to ", node     
      send_message(node, msg)
      msg.last_location = msg.current_location
      msg.current_location = node.id



   #returns the closest proceeding node to the destination of the message of which this node knows 
   #(closest to msg.dest within self.fingers) 
   def closest_preceding_node(self, msg):
      for i in range(len(self.fingers)-1,-1,-1): #loop backwards
         if between(self.fingers[i].id, self.id , msg.dest):
            return self.fingers[i]

      return self



   def __str__(self):
      return "Node %d (%d,%d,%d,%d)" % (self.id, self.fingers[0].id, self.fingers[1].id, self.fingers[2].id, self.fingers[3].id)







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
         print log(SIZE,2), "links"
         for j in range(log(SIZE,2)):
            print "link to :", (i+(2**j))%SIZE, i, j
            self.nodes[i].fingers.append(self.nodes[(i+(2**j))%SIZE])



      #test messages
      send_message(self.nodes[1], Message(1,14,0)) #from 1 to 14 at t=0
      send_message(self.nodes[35], Message(35,11,2)) #from 1 to 14 at t=0
      send_message(self.nodes[42], Message(42,9,3)) #from 1 to 14 at t=0  
      send_message(self.nodes[14], Message(14,8,3)) #from 1 to 14 at t=0
      send_message(self.nodes[17], Message(17,14,5)) #from 1 to 14 at t=0    
      

   def tick(self):
      self.t += 1
      print "tick", self.t
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

