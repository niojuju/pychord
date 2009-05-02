"""
Chord Logging / Metrics collection tool

	- Set up metrics-collection & display for following:
		- Number of active/inactive nodes
		- Min/Avg/Max length of searches
	- Set up logging messages on GUI
		- Message @ start-nodes, @ destination-nodes (and hops), 
		- Joins, Leaves, 
		- Message-deaths?/time-outs

"""

from chordTest import *

DISPLAY_INTERVAL = 5

class chordLogger:
    """ Logs simulation messages to visualizer +/ file + console
       Carries out metrics analysis  
    """
   
    def __init__(self):
        self.t = 0

        # Instantiate log-file / viz.
        if VISUALIZE is True: 
           print "[chordLogger] Will visualize"
           #viz = ChordWindow()
        if LOG_TO_FILE is True: 
           print "[chordLogger] Will log messages to file"
           """ Open file and stuff """
           
        # Initialize metrics collection variables
        self.total_joins = 0
        self.total_leaves = 0
        self.total_fails = 0
        self.total_msgs_reached = 0
        self.total_hops_taken_for_reach = 0
        self.total_hops_taken_before_failure = 0
        self.total_msgs_failed = 0
        
        self.current_nodes_in_network = 0
        self.avg_hops_to_reach = 0
        self.avg_hops_before_failure = 0
        
        self.hot_sources = []
        self.hot_destinations = []

    def log(self, logString):
       # to console
       print logString 
       # to viz
       if VISUALIZE is True: 
           print "[chordLogger] Will write to viz: ", logString 
       # to file
       if LOG_TO_FILE is True: 
           print "[chordLogger] Will write to file: ", logString 

    def update_state(self):
        """ Updates internal state variables a.k.a. Metrics collected """
        self.current_nodes_in_network = self.total_joins - self.total_leaves - self.total_fails
        if self.total_msgs_reached != 0:
            self.avg_hops_to_reach = self.total_hops_taken_for_reach / self.total_msgs_reached
        if self.total_msgs_failed != 0:
            self.avg_hops_before_failure = self.total_hops_taken_before_failure / self.total_msgs_failed        
        print "[chordLogger] Updating internal state variables " 
 
    def print_state(self):
        print "current_nodes_in_network ", self.current_nodes_in_network
        print "avg_hops_to_reach ", self.avg_hops_to_reach
        print "total_msgs_reached ", self.total_msgs_reached
        print "total_fails ", self.total_fails
        
        
 
    def tick(self):
        self.t += 1
        self.update_state();
        
        if (self.t % DISPLAY_INTERVAL) == 0:
            print "[chordLogger] time: ", self.t
            self.print_state();
      
    """
    Network Log Methods:
    - log_join(ID)
    - log_leave(ID)
    - log_msg_reached(src, dest, hops)
    - log_msg_failed(src, dest, hops, failed_at, trying_to_reach)
    - log_message_route -- not sure
    """
   
    def log_join(self, nodeID):
       self.total_joins += 1
       self.log(("Node Join: ", nodeID))
       
    def log_leave(self, nodeID):
       self.total_leaves += 1
       self.log(("Node Leave: ", nodeID))

    def log_fail(self, nodeID):
       self.total_fails += 1
       self.log(("Node Fail: ", nodeID))
       
    def log_msg_reached(self, src, dest, hops):
       self.total_msgs_reached += 1
       self.total_hops_taken_for_reach += hops
       self.log(("Message from ", src, " to ", dest, " reached in ", hops, " hops"))

    def log_msg_failed(self, src, dest, hops, failed_at, trying_to_reach):
       self.total_msgs_failed += 1
       self.total_hops_taken_before_failure += hops
       self.log(("Message from ", src, " to ", dest, " failed at node ", failed_at, " trying to reach", trying_to_reach))
       
   
if __name__ == "__main__":
    log = chordLogger()
    print "[chordLogger] instance made"
    log.tick()
    
    log.log_join('1')
    log.log_join('2')
    log.tick()

    log.tick()
    log.tick()
    log.tick()
    
    log.log_join('3')
    log.log_join('4')
    log.tick()
    
    log.tick()
    log.tick()
    log.tick()
    
    log.log_msg_reached('1', '2', 1)
    log.tick()

    log.tick()
    log.tick()
    log.tick()
    
    log.log_msg_failed('1', '4', 2, '2', '3')
    log.tick()
    
    log.tick()
    log.tick()
    log.tick()
    
    