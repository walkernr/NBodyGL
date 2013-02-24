# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 20:48:29 2013

@author: Nick Walker
"""

#mouse messes up keyboard

import sys

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from AstroObject_V1_0 import *
from Newton_V1_0 import *
from Ship_V1_0 import *
from numpy import *
from random import *

camera = [10.0, 0.0, 0.0]
target = [0.0, 0.0, 0.0]
transverse = [0.0, 1.0, 0.0]
frange = 10000.0
lambient =  [0.0, 0.0, 0.0, 1.0]
ldiffuse =  [1.0, 1.0, 1.0, 1.0]
lspecular =  [1.0, 1.0, 1.0, 1.0]
lmodelambient = [0.2, 0.2, 0.2, 1.0]
lposition =  [1.0, 1.0, 1.0, 0.0]

ship = Ship()

sun = AstroObject(mass = 100.0, density = 10.0, position = [0.0, 0.0, 0.0], velocity = [0.0, 0.0, 0.0], angular_position = 0.0, angular_velocity = 2.0)

m = 10

objects = []
objects.append(sun)

for n in range(m):
    r = uniform(5, 10)
    a = uniform(0, 2) * pi
    body = AstroObject(mass = uniform(.1, .25), density = uniform(1, 2), position = [r*cos(a), r*sin(a), 0.0], velocity = [0.0, 0.0, 0.0], angular_position = 0.0, angular_velocity = 2.0)
    body.setMomentum(body.getMass() * getCentripetalVelocity(sun, body))
    objects.append(body)

def Calculations():
    global objects
    objects = updateCollisions(objects)
    updatePositions(objects)
    glutPostRedisplay()

def drawAxes():
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(4.0, 0.0, 0.0)
    glEnd()
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 4.0, 0.0)
    glEnd()
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 4.0)
    glEnd()
    for n in range(10):
        glBegin(GL_LINE_LOOP)
        angle = 0.0
        for m in range(360):
            glVertex3f(cos(angle) * (n + 1), sin(angle) * (n + 1), 0.0)
            angle = angle + pi / 180.0
        glEnd()

def forward():
    ship.forward()
    Calculations()

def backward():
    ship.backward()
    Calculations()

def stop():
    ship.stop()
    Calculations()

def passive(x, y):
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    ship.facing(x, y, w, h)

def init():
    localview = [0.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, lambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, ldiffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lspecular)
    glLightfv(GL_LIGHT0, GL_POSITION, lposition)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, lmodelambient)
    glLightModelfv(GL_LIGHT_MODEL_LOCAL_VIEWER, localview)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(ship.getCamera()[0], ship.getCamera()[1], ship.getCamera()[2], ship.getTarget()[0], ship.getTarget()[1], ship.getTarget()[2], 0.0, 0.0, 1.0)
    glLightfv(GL_LIGHT0, GL_POSITION, lposition)
    drawAxes()
    for object in objects:
        object.updateAstro()
    glutSwapBuffers()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(w)/h, .01, 10000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard(key, x, y):
    if key == 'i':
        ship.rotateUp()
    elif key == 'j':
        ship.rotateLeft()
    elif key == 'k':
        ship.rotateDown()
    elif key == 'l':
        ship.rotateRight()
    elif key == 'w':
        ship.forward()
    elif key == 's':
        ship.backward()
    elif key == 'a':
        ship.left()
    elif key == 'd':
        ship.right()
    elif key == 'q':
        ship.down()
    elif key == 'e':
        ship.up()
    elif key == '+':
        ship.zoomIn()
    elif key == '-':
        ship.zoomOut()
    elif key == '':
        sys.exit()
    elif key == ']':
        r = uniform(5, 10)
        a = uniform(0, 2) * pi
        body = AstroObject(mass = uniform(.1, .25), density = uniform(1, 2), position = [r*cos(a), r*sin(a), 0.0], velocity = [0.0, 0.0, 0.0], angular_position = 0.0, angular_velocity = 2.0)
        body.setMomentum(body.getMass() * getCentripetalVelocity(sun, body))
        objects.append(body)
        glutPostRedisplay()
    elif key == '[':
        if len(objects) > 0:
            objects.pop()

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):
            glutIdleFunc(forward)
    elif button == GLUT_RIGHT_BUTTON:
        if(state == GLUT_DOWN):
            glutIdleFunc(backward)
    elif button == GLUT_MIDDLE_BUTTON:
        if(state == GLUT_DOWN):
            glutIdleFunc(stop)

glutInit(sys.argv)
glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize (512, 512)
glutInitWindowPosition (100, 100)
glutCreateWindow('NBODY')
init()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutPassiveMotionFunc(passive)
glutIdleFunc(Calculations)
glutMainLoop()