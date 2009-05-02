from math import log
# maximum size of teh chord network / size fo the address space
SIZE = 64


#a global dictionary to hold the messages that are to be processed by the nodes at this timestep
#key = node this event is to be handled by
#val = a list of events. each event is some sort of event description that is interpreted by teh node 
#at each timestep the nodes will handle teh messages from the last round and create new events for teh next round
chord_messages = {}




# simple helper function.  returns true if x lies between i and j on the adress space ring
def between(x, i, j):
   if i <= j:
      return x >= i and x <=j
   else: #this spans the origin
      return x >= i or x<= j






#A simple class to hold some data representing a message on teh network
class Message:

   def __init__(self, src, dest, time_stamp=None, transfer_time=3, content=""):
      self.dest = dest              
      self.src = src                
      self.init_time =time_stamp            # Start-time 
      self.t = time_stamp                   # ??
      self.content = content                # Content -- Some string msg. here
      self.current_location = src   
      self.last_location = src

      self.num_hops = 0                     # Hops till now
      self.transfer_time = transfer_time    # Max-hops?
      self.route = []


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

   def __init__(self, id, network=None):
      self.id = id
      self.fingers = []
      self.predecessor = None
      self.time = 0

      #the pending list will hold info so that we can remember what requests we are still waiting for
      #when we initialize a search or join well add a reminder here until we receive an answer
      #we will always put a time-stamp with each request when we put it in here so that we can know 
      #when to stop waiting/label the request failed by exceeded TTL
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
            msg.route.append(self.id)
            if self.find_successor(msg): #returns value only if dest (successor) is reached
               pass
               #print "Home:", self, msg
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
      
      from pprint import pprint
      #route to next closest
      node = self.closest_preceding_node(msg)
      print self, "to", msg.dest,  "closest predesessor (routed to):", node
      for f in self.fingers:
         print f

      msg.t = self.time 
      #print "routing to ", node     
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
      return "Node %d " % (self.id)

   def __rerp__(self):
      return self.__str__()





class Network:

   def __init__(self, size):
      self.nodes = []
      self.t = 0
      self.size = size

      #init nodes
      for i in range(size):
         self.nodes.append(Node(i))
      
      #init routing tables
      for i in range(size):
         self.nodes[i].fingers = []
         for j in range(log(size,2)):
            self.nodes[i].fingers.append(self.nodes[(i+(2**j))%size])


      self.add_messages([Message(28,11)])

   def add_messages(self, list_of_messages):
      for msg in list_of_messages:
         msg.t = self.t+1
         send_message(msg.src, msg)
      

   def tick(self):
      self.t += 1
     # print "tick", self.t
      for n in self.nodes:
         n.tick(self.t)

   def make_topology(self):
      print "making topology"
      
   def add_joins(self, node_joins):
      for n_join in node_joins:
         print "node", n_join[0].id, "joining at contact node:", n_join[0]
         
   def add_leave(self, node_leaves):
      for nl in node_leaves:
         print "node", nl.id, "leaving"
         
   def add_fails(elf, node_fails):
      for nf in node_fails:
         print "node", nf.id, "failing"
      
      
   def make_topology(self):
      print "making topology"


if __name__ == "__main__":
   test = Network(32)
   test.tick()
   test.tick()
   test.tick()
   test.tick()
   test.tick()
   test.tick()
   test.tick()

