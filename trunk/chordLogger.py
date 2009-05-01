"""
Analysis it does:
    ??
"""

from chordTest import *

class chordLogger:
   """ Logs simulation messages to visualizer +/ file + console
       Carries out metrics analysis  
   """
   
   def __init__(self):
       self.t = 0

       if VISUALIZE is True: 
           print "[chordLogger] Will visualize"
           #viz = ChordWindow()
       if LOG_TO_FILE is True: 
           print "[chordLogger] Will log messages to file"
           """ Open file and stuff """

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
       print "[chordLogger] Updating internal state variables " 
 
   def tick(self):
      self.t += 1
      update_state();
      print "[chordLogger] time: ", self.t
      
   """
   Network Log Methods:
   - log_join(ID)
   - log_leave(ID)
   - log_msg_reached(src, dest, hops)
   - log_msg_failed(src, dest, hops, failed-at, failed-to-reach)
   """

   """ 
   def log_leave(self, nodeID):
       self.
   , log_join, log_messgage_reached, log_message_fail, log_message_route
   """
   
if __name__ == "__main__":
    log = chordLogger()
    print "[chordLogger] instance made"
    log.tick()