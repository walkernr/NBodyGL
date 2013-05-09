# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 20:48:29 2013

@author: Nick Walker

This program simulates the motion of an N-Body system and allows for traversal with keyboard and mouse input

Copyright (c) 2013 Nicholas Walker

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

#check collision table, collisions are still fucked
#sun keeps disappearing
#pyassimp is a dick

import sys

sys.path += ['.']

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from AstroObject_V1_5 import *
from Newton_V1_5 import *
from Ship_V1_5 import *
from Texture_V1_5 import *
from numpy import *
from random import *
from time import *

from ctypes import util
try:
    #this is for compiling an exe for use with windows
    from OpenGL.platform import win32
except AttributeError:
    pass

#bool values used for arguments
collisions = True
deletion = True
eccentric = False
binary = False
teapots = False
start = time()
frames = 0.0

#number of planets
if len(sys.argv) > 1:
    p = int(sys.argv[1])
else:
    p = 10

#number of orbital rings
if len(sys.argv) > 2:
    s = int(sys.argv[2])
else:
    s = 10

#turn off collisions
if '-c' in sys.argv:
    collisions = False

#turn off boundaries (auto-deletion)
if '-d' in sys.argv:
    deletion = False

#turn on eccentric orbits
if '-e' in sys.argv:
    eccentric = True

#turn on a binary star system
if '-b' in sys.argv:
    binary = True

if '-t' in sys.argv:
    teapots = True

#print usage
if '-u' in sys.argv:
    print 'usage:' + '\n' + 'ARGUMENTS' + '\n' + '=========' + '\n' + 'int[1]: number of planets' + '\n' + 'int[2]: number of orbital rings' + '\n' + '-c: no collisions' + '\n' + '-d: no deletion at boundaries' + '\n' + '-e: more eccentric orbits' + '\n' + '-b: binary star system' + '\n' + '-t: teapots' + '\n' + 'KEYBOARD' + '\n' + '========' + '\n' + 'w,a,s,d,q,e: move ship about system' + '\n' + 'esc: quit the program' + '\n' + '[,]: remove and add planets' + '\n' + 'p: pause/play'

#the position of the camera is set at the edge of the system
camera = [float(s) + 2.0, 0.0, 0.0]
#the point the camera is looking at is set to the center of the system
target = [0.0, 0.0, 0.0]
#the up vector determines what is up
up = [0.0, 0.0, 1.0]
#the maximum viewing range
frange = 1000.0
#ambient light vector
lambient =  [0.2, 0.2, 0.2, 1.0]
#diffuse light vector
ldiffuse =  [0.5, 0.5, 0.5, 1.0]
#specular light vector
lspecular =  [0.5, 0.5, 0.5, 1.0]
#light model ambient vector
lmodelambient = [0.2, 0.2, 0.2, 1.0]
#light position is set a little bit up the z axis
lposition =  [0.0, 0.0, 0.0, 0.0]
#fog color
fog  = [.05, .05, .05]

fx = 256
fy = 256

def skybox(bounds):
    glPushMatrix()
    glRotatef(210.0, 0, 0, 1)
    glBindTexture(GL_TEXTURE_2D, textures[len(textures) -1])
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, bounds, 50, 50)
    glPopMatrix()

#initialize our camera, which is a ship, because we're in space
ship = Ship(camera, target, up)

#this makes it so everything starts static
running = False

#the list of objects in the system
objects = []

def createSystem():
    sun = None
    sun_a = None
    sun_b = None

    #if there is only one star, we make one star
    if not binary:
        sun = AstroObject(mass = 100.0 * s, density = 100.0, position = [0.0, 0.0, 0.0], velocity = [0.0, 0.0, 0.0], angular_position = 0.0, angular_velocity = 2.0, texture = textures[0], teapot = teapots, star = True)
        objects.append(sun)

    #but if there are two, we make two
    if binary:
        sun_a = AstroObject(mass = 50.0 * s, density = 100.0, position = [0.0, -2.0, 0.0], velocity = [0.0, 0.0, 0.0], angular_position = 0.0, angular_velocity = 2.0, texture = textures[0], teapot = teapots, star = True)
        sun_b = AstroObject(mass = 50.0 * s, density = 100.0, position = [0.0, 2.0, 0.0], velocity = [0.0, 0.0, 0.0], angular_position = 0.0, angular_velocity = 2.0, texture = textures[0], teapot = teapots, star = True)
        sun_a.setMomentum(sun_a.getMass() * getCentripetalVelocity(sun_b, sun_a) / sqrt(2))
        sun_b.setMomentum(sun_b.getMass() * getCentripetalVelocity(sun_a, sun_b) / sqrt(2))
        objects.append(sun_a)
        objects.append(sun_b)

    #loop to make all of the initial planets
    for n in range(p):
        makeObject(sun, sun_a, sun_b)

    return sun, sun_a, sun_b

#this is where a planet is generated
def makeObject(sun, sun_a, sun_b):
    global objects
    #if there is only one star, planets can be generated much closer to the center of the system
    if not binary:
        r = uniform(4, s)
    if binary:
        r = uniform(6, s)
    a = uniform(0, 2) * pi
    body = AstroObject(mass = uniform(.0001, .001), density = uniform(.002, .004), position = [r*cos(a), r*sin(a), 0.0], velocity = [0.0, 0.0, 0.0], angular_position = 0.0, angular_velocity = 2.0, texture = textures[randint(1,10)], teapot = teapots, rings = choice([textures[len(textures) - 2], textures[len(textures) - 3], None, None, None, None]))
    #the initial momentum will be close to the centripetal velocity of the object in circular motion
    if not binary:
        body.setMomentum(body.getMass() * getCentripetalVelocity(sun, body) * uniform(.9, 1.1))
    #if there are two stars, the momentum is calculated relative to the center of mass of the system
    if binary:
        cm = AstroObject()
        cm.setMass(sun_a.getMass() + sun_b.getMass())
        cm.setPosition((sun_a.getMass()* sun_a.getPosition() + sun_b.getMass() * sun_b.getPosition()) / (sun_a.getMass() + sun_b.getMass()))
        body.setMomentum(body.getMass() * getCentripetalVelocity(cm, body) * uniform (.9, 1.1))
    if eccentric:
        body.setMomentum(body.getMomentum() * uniform(.5, 1.5))
    objects.append(body)

#idle function to update all object positions and camera facing
def Calculations():
    global objects
    global test
    global frames
    global start
    if running:
        update(objects)
        if collisions:
            objects = getCollisions(objects, teapots)
        if deletion:
            objects = deleteObjects(objects, float(s) + 2)
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    ship.facing(fx, fy, w, h)
    glutPostRedisplay()
    frames = frames + 1
    if frames > 100:
        elapsed = time() - start
        sys.stdout.write('\r')
        sys.stdout.write(str(frames / elapsed))
        sys.stdout.flush()
        frames = 0
        start = time()

#calls to move the ship, used by mouse function
def forward():
    Calculations()
    ship.forward()

def backward():
    Calculations()
    ship.backward()

def shoot():
    projectile = AstroObject(mass = .001, density = .004, position = ship.getCamera(), velocity = 1. * ship.getFacingVector(), texture = textures[0], teapot = teapots)
    projectile.setRadius(.01)
    objects.append(projectile)

#passive mouse function that gets the mouse position when it is moved
def motion(x, y):
    global fx
    global fy
    fx = x
    fy = y

def init():
    global s
    #number of orbital rings set to the second integer command line input
    if len(sys.argv) > 2:
        s = int(sys.argv[2])
    #default is ten
    else:
        s = 10
    #lighting is setup
    glLightfv(GL_LIGHT0, GL_AMBIENT, lambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, ldiffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lspecular)
    glLightfv(GL_LIGHT0, GL_POSITION, lposition)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, lmodelambient)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, fog)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, 1)
    glFogf(GL_FOG_END, 1000)
    #display list for the axes and the orbitals
    glNewList(1, GL_COMPILE)
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, 0)
    glMaterialfv(GL_FRONT, GL_AMBIENT, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, .5)
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
    #loops are like polygons with 360 sides
    for n in range(int(s) + 2):
        glBegin(GL_LINE_LOOP)
        angle = 0.0
        for m in range(360):
            glVertex3f(cos(angle) * (n + 1), sin(angle) * (n + 1), 0.0)
            angle = angle + pi / 180.0
        glEnd()
    skybox(frange / 4)
    glPopMatrix()
    glEndList()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    #the camera is located where it is and is facing the target with the positive z axis up
    gluLookAt(ship.getCamera()[0], ship.getCamera()[1], ship.getCamera()[2], ship.getTarget()[0], ship.getTarget()[1], ship.getTarget()[2], ship.getUp()[0], ship.getUp()[1], ship.getUp()[2])
    glLightfv(GL_LIGHT0, GL_POSITION, lposition)
    #the display list is called
    glCallList(1)
    #every object's position is updated accordingly
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    for object in objects:
        object.updateAstro()
    glDisable(GL_CULL_FACE)
    glutSwapBuffers()

#modifies the perspective for when the window size changes
def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(w)/h, .01, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

#keyboard commands
def keyboard(key, x, y):
    global running
    if key == 'w':
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
    elif key == ' ':
        shoot()
    elif key == '':
        sys.exit()
    elif key == ']':
        makeObject(stars[0], stars[1], stars[2])
    elif key == '[':
        if len(objects) > 1:
            objects.pop()
    elif key == 'p':
        running = not running

#the mouse is used to control the ship
def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):
            glutIdleFunc(forward)
        elif (state == GLUT_UP):
            glutIdleFunc(Calculations)
    elif button == GLUT_RIGHT_BUTTON:
        if (state == GLUT_DOWN):
            glutIdleFunc(backward)
        elif (state == GLUT_UP):
            glutIdleFunc(Calculations)
    elif button == GLUT_MIDDLE_BUTTON:
        if (state == GLUT_DOWN):
            shoot()

glutInit(sys.argv)
glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize (1024, 576)
glutInitWindowPosition (100, 100)
glutCreateWindow('NBODY')
#this is the list with the IDs of the textures used for objects
textures = textureList()
init()
stars = createSystem()
glEnable(GL_TEXTURE_2D)
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutPassiveMotionFunc(motion)
glutMotionFunc(motion)
glutIdleFunc(Calculations)
glutMainLoop()