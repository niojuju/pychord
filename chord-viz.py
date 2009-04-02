import pyglet
from pyglet.window import Window, key
from pyglet.gl import *
from math import sin, cos, radians
from random import randint

from pychord import *




EDGE_COLOR = (1,1,1)
NODE_COLOR = (0,1,0)




STEP_TIME = 1.0












def drawLine(p1,p2, width=0.5):
   glLineWidth(width)
   glBegin(GL_LINES)
   glVertex2f(p1[0], p1[1])
   glVertex2f(p2[0], p2[1])      
   glEnd()
   
def drawTriangle(pos, w, h, style=GL_TRIANGLES):
    points = [pos[0]-w/2, pos[1], pos[0]+w/2, pos[1], pos[0], pos[1]+h]
    glBegin(GL_TRIANGLES)
    while len(points):
      glVertex2f(points.pop(), points.pop())
    glEnd()

def drawCircle(pos=(0,0), radius=1.0):
   x, y = pos[0], pos[1]
   glPushMatrix()
   glTranslated(x,y, 0)
   glScaled(radius, radius, 1.0)
   gluDisk(gluNewQuadric(), 0, 1, 16,1)
   glPopMatrix()






class ChordWindow(Window):

   def __init__(self, chord):
      config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True,)
      super(ChordWindow, self).__init__(caption="Chord visualization", config=config, fullscreen=True)
   
      #the chord model
      self.chord = chord

   def on_resize(self, width, height):
       glViewport(0, 0, width, height)
       glMatrixMode(gl.GL_PROJECTION)
       glLoadIdentity()
       ar = float(width)/height
       glOrtho(-12*ar, 12*ar, -12, 12, -1, 1)
       glMatrixMode(gl.GL_MODELVIEW)


   def get_node_pos(self, i):
      try:
         #print "i as int", self.chord.nodes[i]
         n, size = self.chord.nodes[i].id, float(SIZE)
         return cos(radians( n/size*-360+90))*10,sin(radians( n/size*360+90))*10
      except:
         n, size = i.id, float(SIZE)
         return cos(radians( n/size*-360+90))*10,sin(radians( n/size*360+90))*10


   def on_key_press(self, symbol, modifiers):
      if symbol == key.ESCAPE:
         pyglet.app.exit()
      elif symbol == key.SPACE:
         print "tick", self.chord.t 
         self.chord.tick()




   def on_draw(self):
      global chord_messages
      self.clear()

      #draw connections
      glColor3f(*EDGE_COLOR)
      for node in self.chord.nodes:
         x,y = self.get_node_pos(node)
         for dest in node.fingers:
            x2,y2 = self.get_node_pos(dest)
            drawLine((x,y),(x2,y2))


      #draw nodes
      glColor3f(*NODE_COLOR)
      for node in self.chord.nodes:
         n, size = node.id, float(SIZE)
         x,y = self.get_node_pos(n)
         drawCircle((x,y),.2)


      #draw current messages
      
      print chord_messages
      for node in chord_messages:
         print "msgs of", node
         for m in chord_messages[node]:
    
            if m.t > self.chord.t:
               continue #dont handle messages that are still waiing to start

            glColor3f(0,0,1)
            print self.chord.t, m.last_location, m.current_location
            fro = self.get_node_pos(m.last_location)
            to =  self.get_node_pos(m.current_location)

            if m.content == "OK":
               glColor3f(1,1,0) #direct communication/response to src


            drawCircle(to,.2)                     
            #drawTriangle(fro, .2,.2)
            drawLine(fro,to,4)

      self.flip()




if __name__ == "__main__":
   test = ChordTest()
   win = ChordWindow(test)
   pyglet.app.run()
