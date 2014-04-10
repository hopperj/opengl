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

def GameLoop():

    glClear(GL_COLOR_BUFFER_BIT)
    

    glColor3f(0.25, 0.75, 0.5)
    glBegin(GL_QUADS)
    
    glVertex2f(0,0)
    glVertex2f(0,64)
    glVertex2f(64,64)
    glVertex2f(64,0)
    

    glEnd()
    glFlush()


if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(640,480)
    glutCreateWindow("OpenGL Testing")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(GameLoop)
    initFun()
    glutMainLoop()
