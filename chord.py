NUM_BITS = 16 

from random import randint, random, choice, paretovariate 
from pprint import pprint



#helper function for determining whether a key in teh identifier sapce falls between to others
#  returns true if x is strictly between i and j (x comes after i and before j, not equal to either i or j)
#  also returns False if x is None or False
def between(x, i, j):
    if not x:
        return False
    
    if i <= j:
       return x > i and x <j
    else: #this spans the origin
       return x > i or x<j

message_ids = 0


class Message:
    
    def __init__(self, src, dest, type="lookup", callback=None, data=None):
        global message_ids
        self.src = src
        self.dest = dest
        self.route = [src]
        self.type = type
        self.callback = callback
        self.data = data 
        self.status = 'routing'
        self.id = message_ids +1
        message_ids += 1
        
    def fail(self):
        self.status = 'failed'
        print "FAILED MESSAGE:", self.src, '->', self.dest, self.route, self.type
        
    def arrive(self):
        #print self.type,"arrived", self.src, self.dest
        self.status = 'arrived'
        if self.callback:
            self.callback(self)
        

    def route_to(self, node_id):
        self.route.append(node_id)
        if len(self.route)>3 and self.route[-1] == self.route[-2] == self.route[-3]: #were stuck..failed message
            self.fail()
            

watching = {}

class Node:
    
    def __init__(self, id, nw, ttl=-1, stabilize_freq=0.1, finger_fix_freq=0.1):
    # id:  this nodes id/key in the identifier space of teh network
    # nw:  the network teh node is participating in (so we can get node objects by ID)
    # ttl: time to live.  if negative lives forever, decremented each tick. once ttl = 0 node dies
    # predec:   the node's predecessor (from its point of view)
    # fingers:  teh finger table (holds node ID's)
    # messages: a list of messages this node owns and handles at each tick
    # stabilize_freq/finger_fix_freq: used for determining when/whether to run stabilization protocol
    
        self.id = id
        self.nw = nw #so we can get other node objects by ID
        self.ttl = ttl
        self.predec = None
        self.fingers = [None for i in range(NUM_BITS)]
        self.messages = []
        
        #used for determining when/whether to run stabilization protocol
        self.stabilize_freq = stabilize_freq
        self.finger_fix_freq = finger_fix_freq
        
        
        self.entry = -1
        
    def __str__(self):
    #so that we can print or cast the node to a string
        return "Node: " + str(self.id)
        
    
    def die(self):
        self.predec = None
        self.messages = None
        self.fingers = None
    
    def tick(self):
    #is called at each timestep of the network
    #performs one round of actions
        
        #handle this nodes messages 
        self.handle_messages()
            
        #unless we have succesfully joined teh network, we cant do maintanance
        if not self.fingers[0]:
            return
            
        #perform some maintanance
        if random() < self.stabilize_freq:
            self.stabilize()
        if random() < self.finger_fix_freq:
            self.fix_fingers()
            
        if random() < 0.1:
            self.send_message(self.nw.random_node().id)
        
        #one step closer to death..such is life
        self.ttl -= 1
        
        
    def handle_messages(self):
    #iterates over all the messages this node owns
    #  if a message is routing:
    #  do next hop and remeber the message for the next round
    
        still_alive = []
        for msg in self.messages:
            if msg.status == 'routing':
                self.route_message(msg)
                still_alive.append(msg)
            if msg.status == 'arrived':
                pass #log arrive here?       
            if msg.status == 'failed':
                pass #log fail here?
            
        #only remember teh ones that are still going
        self.messages = still_alive
            
    
    
    """
    Routing Protocol:
    ################################################################################################
    """
    
        
    def send_message(self, dest, type='lookup', callback=None, data=None):
    #Creates a new message orginating at this node
    #  dest: key/node this is meant for, message will get routed to dest or successor if no node at dest
    #  type: optional field describing what kind of message this is (used in visualizer to set color)
    #  callback: optional function pointer. Teh calback will be called with message as argument when it arrives at final destination
    #  data: optional anything, can be used to attach various data (e.g. finger index so callback knows which finger to update on response)
        if dest == self.id:
            return #no ned to send yourself a message
        m = Message(self.id, dest, type=type, callback=callback, data=data)
        self.messages.append(m)
        #print "sending new message", self.id, m.src, dest,m.dest, type, m.route, m.id
        return m
    
    def route_message(self, msg):
    #This function is called every tick by each node for every message it started
    #It routes each message one step closer until it reaches the 'successor'.
    #Messages are rourted until their location = dest or the first node with id > dest.
        
        #get the node our message is currently at
        current_node = self.nw.get_node(msg.route[-1])
        
        #maybe the node we are looking for doesnt exist in the network...the routing fails
        if (not current_node) or (not current_node.fingers[0]) :
            msg.fail()
            print " FAIL  :", msg.route, "from:", msg.src, " to:", msg.dest, msg.type            
            return False

        
        #check whether the current node is immediate predecesor.  in this case the target is its successor
        if between(msg.dest, current_node.id, current_node.fingers[0]+1):
            msg.route_to(current_node.fingers[0])
            msg.arrive()
            #print "arrived"
            return current_node.fingers[0]
        
        #we are not there yet, in this case we make a hop to the closest node the current one knows about
        else:
            next_node_id = current_node.closest_preceding_finger(msg.dest)
            msg.route_to(next_node_id)
            return next_node_id
        
        raise Exception, "Routing Error"
        


    def closest_preceding_finger(self, id):
    #Returns teh closest node to id this node knows about
    #Iterates over fingers in reverse and returns as soon as one is preceeding id.
    #Returns this nodes ID if no preceeding finger is known
    
        for finger in reversed(self.fingers): 
            if between(finger, self.id , id): #and self.nw.get_node(finger):
                if not self.nw.get_node(finger):
                    self.fix_finger(self.fingers.index(finger), foreign_find=True)
                return finger
                
        return self.id 
    
    

    
    
    
    """
    Join Protocol:
    ################################################################################################
    """
    def init_join(self, entry_node):
        self.entry = entry_node
        if entry_node:
            self.predec = None
            m = entry_node.send_message(self.id, type='join', callback=self.join_response)

    def join_response(self, msg):
        sucessor = self.nw.get_node(msg.route[-1])
        self.fingers[0] = sucessor.id
        sucessor.notify(self.id)
        self.init_fingers()

    def init_fingers(self):
        for finger_index in reversed( range(len(self.fingers)) ): 
            self.fix_finger(finger_index)
                    
    def finger_response(self, msg):
        self.fingers[msg.data] = msg.route[-1]
    
    
    
    """
    Stabilization Protcol:
    ################################################################################################
    """
    def fix_fingers(self):
        finger_index = randint(0,NUM_BITS-1)
        self.fix_finger(finger_index)
        #for i in range(NUM_BITS):
        #    if not self.nw.get_node(self.fingers[i]):
        #        self.fix_finger(i, foreign_find=True)

        
    def fix_finger(self, index, foreign_find=False):
        ideal_finger = (self.id + 2**(index)) % 2**NUM_BITS
        self.send_message(ideal_finger, type='finger', callback=self.finger_response, data=index)
 
    def stabilize(self):
        sucessor = self.nw.get_node(self.fingers[0])
        if not sucessor:
            return self.fix_fingers()
        new_sucessor_id = sucessor.predec
        if between(new_sucessor_id, self.id , self.fingers[0]):
            self.fingers[0] = new_sucessor_id
            if self.nw.nodes.has_key(new_sucessor_id):
                self.nw.get_node(self.fingers[0]).notify(self.id)
        
    def notify(self, pre_node):
        if (self.predec == None) or between(pre_node, self.predec, self.id):
            self.predec = pre_node



    



        
        
        
        
from chordLogger import chordLogger
        
class Network:
    
    def __init__(self, logger=None):

        self.name_space_size = 2**NUM_BITS
        self.t = 0

        if logger:
            self.logger = logger
        else:
            self.logger = chordLogger()
        self.nodes = {}

        self.max_size = 500
        self.growing = False 
        
        #parameters for randomization/eventdistribution
        
        #exponential distributin. mostly one node will join per tick.  less often 2 nodes, less often 3 nodes...etc.
        self.concurent_join_alpha = 4
        
        #the rate at which nodes leave/join teh network
        self.churn_rate = 0.05
        
        #the rate at which nodes perform the fix_finger and stabilize protocol
        self.fix_rate = 0.4
        self.stabilize_rate = 0.3
        self.message_rate = 0.6



    def tick(self):
        for n in self.nodes.values():
            n.tick()


    def get_node(self, node_id):
        if node_id in self.nodes:
            return self.nodes[node_id]
        else:
            #print "accessing missing node: ", node_id
            return None
        
    def random_node(self):
        return self.nodes[choice(self.nodes.keys())]
        
    def get_unique_id(self):
        #returns an unused ID
        newID = randint(0,self.name_space_size)
        while self.nodes.has_key(newID):
            newID = randint(0,self.name_space_size)
        return newID
        
        
    def bootstrap(self, num_nodes=3):
    #bootstraps the network with num_nodes inital nodes evenly distriubuted, with predecessors set and fingers pointing at successors
        last_node = None
        for i in range(1,self.name_space_size, self.name_space_size/num_nodes):
            #print "booting node:", i
            self.nodes[i] = Node(i, self)            
            
            if last_node: #set finger table of predecessor to current node
                self.nodes[i].predec = last_node.id #set predecessor
                last_node.fingers = [self.nodes[i].id for x in range(NUM_BITS)]
            last_node = self.nodes[i]
 
        self.nodes[1].predec = last_node.id #predecessor of first node is teh last one
        last_node.fingers = [self.nodes[1].id for x in range(NUM_BITS) ] #finger table fo last node
      
      
    def grow(self, num_nodes):
        self.growing = True
        #keep taking stes to grows teh network using random joins until num_nodes are participating
        while len(self.nodes) < num_nodes:
            self.tick()
            if random() < 0.4:
                id = self.get_unique_id()
                n = Node(id, self)
                
                self.add_node(n) #also returns a hook for the node to join at
                
        
        self.growing = False

    def add_node(self, node):
        node.init_join(self.random_node())
        self.nodes[node.id] = node
        self.logger.log_join(node.id)
        
    def add_random_node(self):
        n = Node(self.get_unique_id(), self)
        self.add_node(n)
        
      
    def remove_node(self, id):
       self.nodes[id].die()
       del self.nodes[id]
       self.logger.log_leave(id) 


    def remove_random(self):
        node = self.random_node()
        self.remove_node(node.id)
        

    def add_messages(self, messages):
       for m in messages:
            self.nodes[m[0]].send_message(m[1], callback=self.log_message_result)
            self.logger.log_msg_sent(*m)
            
    def log_message_result(self, m):
        if m.status == 'arrived':
            self.logger.log_msg_reached(m.src, m.dest, len(m.route))
        if m.status == 'failed':
            self.logger.log_msg_failed( m.src, m.dest, len(m.route), m.route[-1], m.dest)
      
      
    def add_joins(self, node_joins):
       for join in node_join:
            id, ttl = join
            node = Node(id, self, ttl=ttl)
            node.init_join(self.random_node())
            self.add_node(node)
      
    def add_leaves(self, leaves):
       for leave_id in node_join:
            self.remove_node(leave)
      



if __name__ == "__main__":
    chord = Network()
    print "boot"
    chord.bootstrap(3)
    
    print "growing"
    chord.grow(12)
        
    print "DONE"
    
        
