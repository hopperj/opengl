from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos,sin,atan2,sqrt,pi
import sys
from random import random
from time import sleep
from datetime import datetime
import glFreeType


HEIGHT = 480
WIDTH = 640
FPS = 60.0
#our_font = None




def drawRect(x, y, width, height, rotation=0):
    glColor3ub (0, 0, 0)

    glPushMatrix()

    glTranslatef(x, y, 0)
    glRotatef(rotation, 0, 0, 1)


    glBegin(GL_QUADS)

    hh = height/2.0
    hw = width/2.0

    glVertex2f(-hw, -hh)
    glVertex2f(-hw,hh)
    glVertex2f(hw, hh)
    glVertex2f(hw,-hh)


    glEnd()

    glPopMatrix()






class Player():
    
    def __init__(self, x,y, comp=0, points=0):
        self.x = x
        self.y = y
        self.h = 128
        self.w = 32
        self.score = points
        self.speed = 15
        self.AI = comp

        # Left Edge
        self.LE = self.x - self.w/2.0
        # Right Edge
        self.RE = self.x + self.w/2.0
        # Top Edge
        self.ToE = self.y + self.h/2.0
        # Lower Edge
        self.LoE = self.y - self.h/2.0



    def move(self, d):
        if d > self.speed:
            d = self.speed

        self.y += d
        # Left Edge
        self.LE = self.x - self.w/2.0
        # Right Edge
        self.RE = self.x + self.w/2.0
        # Top Edge
        self.ToE = self.y + self.h/2.0
        # Lower Edge
        self.LoE = self.y - self.h/2.0


    def draw(self):
        drawRect(self.x, self.y, self.w, self.h)
        return 1


class Ball():
    
    def __init__(self):
        self.MAX_SPEED = 1.0e0

        self.w = 8
        self.h = 8
        
        self.x = WIDTH/2.0
        self.y = HEIGHT/2.0
        self.speed = 5.0e-2
        self.angle = 0.1#(random()*20.0 - 10.0)


        # Left Edge
        self.LE = self.x - self.w/2.0
        # Right Edge
        self.RE = self.x + self.w/2.0
        # Top Edge
        self.ToE = self.y + self.h/2.0
        # Lower Edge
        self.LoE = self.y - self.h/2.0

    def increase_speed(self):
        #return 0
        if self.speed < self.MAX_SPEED:
            self.speed *= 1.25

    def move(self,dx,dy):
        self.x += dx
        self.y += dy
        # Left Edge
        self.LE = self.x - self.w/2.0
        # Right Edge
        self.RE = self.x + self.w/2.0
        # Top Edge
        self.ToE = self.y + self.h/2.0
        # Lower Edge
        self.LoE = self.y - self.h/2.0
        
    def draw(self):
        drawRect(self.x, self.y, self.w, self.h)
        return 1

class Pong:

    def __init__(self, vsAI=1):
        self.ball = Ball()
        self.P1 = Player(25,HEIGHT/2.0)
        self.P2 = Player(WIDTH-25, HEIGHT/2.0, vsAI)
        
        self.MAX_BALL_ATTENUATION = 0.25

        self.our_font = glFreeType.font_data ("Test.ttf", 16) 


    def keyPressed(self,k, x, y):
        if k == 'w':
            self.P1.move( self.P1.speed)
        elif k == 's':
            self.P1.move(-1.0*self.P1.speed)

    def attenuateAngle(self):

        # Is hitting P1 ( LEFT )        
        if abs( self.ball.x - self.P1.x ) < abs( self.ball.x - self.P2.x ):
            # Detect if the ball is travelling upwards of downwards.
            if sin(self.ball.angle) < 0.0:
                a = (180.0 - self.ball.angle) * ( 1.0 - abs( self.P1.y - self.ball.y ) / (self.P1.h/2.0) )
            else:
                a = (360.0 - (self.ball.angle - 180.0)) * ( 1.0 + abs( self.P1.y - self.ball.y ) / (self.P1.h/2.0) )

        # Is hitting P2
        else:
            if sin(self.ball.angle) < 0.0:
                print "moving upwards"
                a = (180.0 - self.ball.angle) * ( 1.0 + abs( self.P1.y - self.ball.y ) / (self.P1.h/2.0) )
            else:
                print "moving downwards"
                a = (180.0 + ( 360.0 - self.ball.angle)) * ( 1.0 - abs( self.P1.y - self.ball.y ) / (self.P1.h/2.0) )

        self.ball.angle = a % 360.0

    def update(self):

        self.printScore()

        # Let computers have a turn
        for p in [ self.P1, self.P2 ]:
            if p.AI:
                a = self.ball.y - p.y
                p.move( a )


        nx = self.ball.speed * cos( self.ball.angle * (pi/180.0) )
        ny = self.ball.speed * sin( self.ball.angle * (pi/180.0) )


        self.moveBall(nx,ny)


    def printScore(self):
        cnt1 = 0.051
        """
        glColor3ub (0xff, 0, 0)
        glPushMatrix()        
        glScalef( 1, 1, 1 )
        self.our_font.glPrint( HEIGHT*0.5, WIDTH*0.5, "%d %d"%(self.P1.score,self.P2.score) )
        glPopMatrix()
        print self.our_font
        """
	# Clear The Screen And The Depth Buffer
	#glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	#glLoadIdentity()					# Reset The View 
	# Step back (away from objects)
	#glTranslatef ( WIDTH/2.0, HEIGHT/2.0, 0 )

	# Red Text
	#glColor3ub (0xff, 0, 0)

	#glPushMatrix ()
	#glLoadIdentity ()

	#glScalef (1, 0.8 + 0.3* cos (cnt1/5), 1)
	#glTranslatef (-180, 0, 0)
	#our_font.glPrint (320, 240, "Active FreeType Text - %7.2f" % (cnt1))
	#glPopMatrix ()

    def moveBall(self,nx,ny):

        if self.ball.RE > self.P2.LE:
            assert  self.P2.ToE == self.P2.y + self.P2.h/2.0



        # Collision RIGHT
        if ( self.ball.RE + nx > self.P2.LE ) and ( self.ball.y+ny < self.P2.ToE ) and ( self.ball.y+ny > self.P2.LoE ):
            nx = self.P2.LE - ( self.ball.x + nx )
            # To prevent a only horizontal game.
            print "RIGHT Old angle:",self.ball.angle
            if abs(self.ball.angle) < 1.0:
                print "RIGHT Generate a random angle"
                self.ball.angle = 180.0 + (random()*20.0 - 10.0)
            else:
                print "RIGHT Attenuating angle"
                self.attenuateAngle()

            print "RIGHT New angle:",self.ball.angle,"\n"
            self.ball.increase_speed()
            self.moveBall( self.ball.x-(self.P2.LE + nx), ny )




        # Collision LEFT
        elif ( self.ball.LE + nx < self.P1.RE ) and (self.ball.y+ny < self.P1.ToE) and (self.ball.y+ny > self.P1.LoE):
            nx = self.P1.RE - ( self.ball.x + nx )
            print "LEFT Old angle:",self.ball.angle
            # To prevent a only horizontal game.
            if 180.0 - abs(self.ball.angle) < 1.0:
                print "LEFT Generate a random angle"
                self.ball.angle = random()*20.0 - 10.0
            else:
                print "LEFT Attenuating angle"
                self.attenuateAngle()

            self.ball.increase_speed()
            print "RIGHT New Angle:",self.ball.angle,"\n"
            self.moveBall( self.ball.x - (self.P1.RE + nx ), ny )




        # Collision TOP
        elif self.ball.ToE + ny > HEIGHT:
            ny = HEIGHT - ( self.ball.y + ny )
            print "TOP Old Angle:",self.ball.angle
            if cos( self.ball.angle * (pi/180.0) ):
                self.ball.angle = (360 - self.ball.angle)%360.0
            else:
                self.ball.angle = (180.0 + self.ball.angle)%360.0
                


            print "TOP New Angle:",self.ball.angle,"\n"

            self.moveBall( nx, self.ball.y - (HEIGHT + ny) )


        # Collision BOTTOM
        elif self.ball.LoE + ny < 0:
            ny = 0.0 - ( self.ball.y + ny )
            print "BOTTOM Old Angle:",self.ball.angle
            #self.ball.angle = (self.ball.angle*-1.0)%360.0
            if cos( self.ball.angle * (pi/180.0) ):
                self.ball.angle = (360.0 - self.ball.angle)%360.0
            else:
                self.ball.angle = (180.0 - ( self.ball.angle - 180.0 ))%360.0
            print "New Angle:",self.ball.angle,"\n"
            self.moveBall( nx, self.ball.y - (ny) )



        else:
            self.ball.move(nx,ny)


        # Score RIGHT
        if ( self.ball.RE > WIDTH ):# and ( self.ball.y+ny > self.P2.ToE ) and ( self.ball.y+ny < self.P2.LoE ):
            print "GOAL!! P1"
            print "P2.x:",self.P2.x, "P2.y:",self.P2.y
            print "ball.x:",self.ball.x, "ball.y:",self.ball.y
            print "nx:",nx,"ny:",ny
            print "ball angle:",self.ball.angle
            print "Height, Width:",HEIGHT,WIDTH
            sys.exit(0)
            self.P1.score += 1
            self.reset()

        # Score LEFT
        elif ( self.ball.LE < 0 ):# and ( self.ball.y+ny > self.P1.ToE ) and ( self.ball.y+ny < self.P1.LoE ):
            print "GOAL!! P2"
            self.P2.score += 1
            self.reset()







        self.draw()
        #sys.exit(0)


    def draw(self):
        self.P1.draw()
        self.P2.draw()
        self.ball.draw()


    def reset(self):
        self.ball = Ball()


pong = Pong()



def initFun():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    #glEnable(GL_TEXTURE_2D)

    #OpenGL clear colour
    # R, G, B, A
    glClearColor(0, 0, 0, 1)
    # Because we are doing 2D
    glDisable(GL_DEPTH_TEST)
    print "Loaded font data"

def GameLoop():
    t1 = datetime.now()
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    pong.update()
    glFlush()
    # For debugging
    #sleep(1)
    t2 = datetime.now()
    d = (t2 - t1).microseconds
    if d*1000.0 < 1.0/FPS:
        sleep ( (1.0/FPS) - d*1000.0 )


if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(640,480)
    window = glutCreateWindow("OpenGL Testing")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)# | GLUT_ALPHA)

    glutDisplayFunc(GameLoop)
    glutIdleFunc( GameLoop )
    print "Set Gameloop!"
    glutKeyboardFunc( pong.keyPressed )
    initFun()
    glutMainLoop()
