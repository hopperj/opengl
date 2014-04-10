from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


HEIGHT = 480
WIDTH = 640

def initFun():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)


    #OpenGL clear colour
    # R, G, B, A
    glClearColor(0, 0, 0, 1)
    # Because we are doing 2D
    glDisable(GL_DEPTH_TEST)

def drawRect(x, y, width, height, rotation=0):

    glPushMatrix()

    glTranslatef(x, y, 0)
    glRotatef(rotation, 0, 0, 1)
    glBegin(GL_QUADS)
    
    hh = height/2.0
    hw = height/2.0

    glVertex2f(-hw, -hh)
    glVertex2f(-hw,hh)
    glVertex2f(hw, hh)
    glVertex2f(hw,-hh)
    

    glEnd()

    glPopMatrix()


def GameLoop():

    rot = 0.0
    while 1:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()


        glColor3f(0.25, 0.75, 0.5)

        #glRotatef(45, 0, 0, 1)
        drawRect(64,64,64,64, rot)
        drawRect(128,128,64,64, rot)        
        glFlush()
        rot += 0.01


if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(640,480)
    glutCreateWindow("OpenGL Testing")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(GameLoop)
    initFun()
    glutMainLoop()
