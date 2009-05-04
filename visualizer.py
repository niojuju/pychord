import pyglet
from pyglet.window import Window, key
from pyglet.gl import *
from math import sin, cos, radians
from random import randint, choice
from pyglet.text import Label

from chord import *

_label = Label("", font_size=8, width=100, multiline=True)
win_width, win_height = 0,0


#drawing helper functins

def drawLine(p1,p2):

   glBegin(GL_LINES)
   glVertex2f(p1[0], p1[1])
   glVertex2f(p2[0], p2[1])      
   glEnd()
   

def drawLines(points,):
   glBegin(GL_LINE_STRIP)
   while(len(points)):
      x,y = node_pos_on_circle(points.pop())
      glVertex2f(x,y)
   glEnd()

def drawTriangle(pos, w, h, style=GL_TRIANGLES):
    points = [pos[0]-w/2, pos[1], pos[0]+w/2, pos[1], pos[0], pos[1]+h]
    glBegin(GL_TRIANGLES)
    while len(points):
      glVertex2f(points.pop(), points.pop())
    glEnd()

def drawRectangle(pos, w, h, style=GL_QUADS):
    points = [pos[0], pos[1], pos[0], pos[1]+h, pos[0]+w, pos[1]+h, pos[0]+w, pos[1]]
    glBegin(GL_QUADS)
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

def drawText(text, pos=(0,0)):
    
    glPushMatrix()
    glTranslated(pos[0],pos[1],0)
    _label.text = text
    _label.draw()
    glPopMatrix()


def node_direction_on_circle(i, scale=1.0):
        size = float(2**NUM_BITS)
        x,y = cos(radians( i/size*-360+90)),sin(radians( i/size*360+90))
        return (x*scale,y*scale)

def node_pos_on_circle(i):
        x,y = node_direction_on_circle(i)
        x,y = x*win_height/3 + win_width/2, y*win_height/3 + win_height/2
        return (x,y)


def drawNode(node):
    
    glPushMatrix()
    x,y = node_pos_on_circle(node.id)
    glTranslated(x,y,0)
    
    glColor4f(.8,1,.8,1)
    drawCircle(radius=10)
    
    glColor4f(1,1,1,1)
    
    label_pos = node_direction_on_circle(node.id, 50)
    drawLine((0,0),label_pos)
    if label_pos[0] >=0:
        glTranslated(3,0,0)
    else:
        glTranslated(-103,0,0)
    drawText(str(node), pos=label_pos)

    glPopMatrix()
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1,1,1,0.4)
    for f in node.fingers:
        if f:
          drawLine((x,y), node_pos_on_circle(f.id))



class ChordWindow(Window):

    def __init__(self):
        try:
            config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True,)
            super(ChordWindow, self).__init__(caption="Chord visualization", config=config, fullscreen=True)
        except:
            super(ChordWindow, self).__init__(caption="Chord visualization", fullscreen=True)

        #initialize a root node/network
        """
        root1 = Node(1)
        root1.join(None)
        root2 = Node(20000)
        root3 = Node(40000)
        root1.fingers = [root2 for i in range(NUM_BITS)]
        root1.predec = root3
        root2.fingers = [root3 for i in range(NUM_BITS)]
        root2.predec = root1
        root3.fingers = [root1 for i in range(NUM_BITS)]
        root3.predec = root2
        self.nodes = {}
        self.nodes[1] = root1
        self.nodes[50] = root2
        self.nodes[180] = root3
        
        self.keys = [1,50,180]
        """
        
        self.nw = Network()
        self.nw.bootstrap(3)
        self.nw.grow(100)
        
        pyglet.clock.schedule(self.update)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        if symbol == key.A:
            newID = randint(0,2**NUM_BITS)
            while self.nodes.has_key(newID):
                newID = randint(0,2**NUM_BITS)
            n = Node(newID)
            i = choice(self.nodes.values())
            n.join(i)
            self.nodes[n.id] = n
            print "added", newID, "at", n.id

        if symbol == key.D:
            self.nw.remove_random()
            print "removed", id

                
    
    def on_draw(self):
        glClearColor(0,0,0,0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        for node in self.nw.nodes.values():
            if node:
                drawNode(node)

        
        for m in chord_messages:
            glLineWidth(1)
            if m.message_type == 'fix':
                glColor4f(0,1,0,1)
            if m.message_type == 'join':
                glColor4f(1,0,1,1)
            if m.message_type == 'init':
                glColor4f(0,1,1,1)
            if m.message_type == 'lookup':
                glColor4f(1,1,0,1)

            if m.status == 'fail':
               glColor4f(1,0,0,0.3)    
               glLineWidth(10)
               drawLines([m.src,m.dest])

            drawLines(m.route)

        self.nw.tick()
            
        
        
   
    def update(self,dt):
        pass
                
            

if __name__ == "__main__":
    win = ChordWindow()
    win_width, win_height = win.width, win.height
    pyglet.app.run()
