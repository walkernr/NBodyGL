# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 01:41:28 2013

@author: Nick Walker

This program simulates the motion of an N-Body system and allows for traversal with keyboard and mouse input

Copyright (c) 2013 Nicholas Walker

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import *
from random import *

class AstroObject:
    """A Class for Creating and Manipulating an Astronomical Object"""

    def __init__(self, mass = .1, density = .2, position = [0.0, 0.0, 0.0], velocity = [0.0, 0.0, 0.0], angular_position = 0.0, angular_velocity = 2, exists = True, texture = None, teapot = False, star = False, rings = None):
        """Initializes Values of Astronomical Object"""
        self._ma = mass
        self._de = density
        self._po = array(position)
        self._ve = array(velocity)
        self._ap = angular_position
        self._av = angular_velocity
        #radius is calculated from mass and density
        self._ra = sqrt(self._ma * 3.0 / 4.0 / self._de / pi)
        #momentum is the mass multiplied by the velocity
        self._p = self._ma * self._ve
        #the moment is the mass multiplied by the position
        self._mo = self._ma * self._po
        self._e = exists
        self._tex = texture
        self._tea = teapot
        self._st = star
        self._ri = rings

    def updateAstro(self):
        """Updates the Astronomical Object and Draws It"""
        #v = p / m : velocity is the ratio of momentum to mass
        self._ve = self._p / self._ma
        #the moment of the object is the mass multiplied by the position, this is used for center of mass
        self._mo = self._ma * self._po
        #the angular position of the object is updated
        self._ap = self._ap + self._av
        glPushMatrix()
        if self._st:
            glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, False)
        glTranslate(self._po[0], self._po[1], self._po[2])
        glRotatef(self._ap, 0.0, 0.0, 1.0)
        if self._tea:
            glDisable(GL_CULL_FACE)
            if self._tex != None:
                glBindTexture(GL_TEXTURE_2D, self._tex)
            glRotatef(90.0, 1.0, 0.0, 0.0)
            glutSolidTeapot(self._ra)
        else:
            if self._ri != None:
                glBindTexture(GL_TEXTURE_2D, self._ri)
                quad_r = gluNewQuadric()
                gluQuadricNormals(quad_r, GLU_SMOOTH)
                gluQuadricTexture(quad_r, GL_TRUE)
                gluPartialDisk(quad_r, self._ra * 1.2, self._ra * 1.4, 50, 50, 0, 360)
            #this binds the texture of the object to the object
            if self._tex != None:
                glBindTexture(GL_TEXTURE_2D, self._tex)
            quad = gluNewQuadric()
            gluQuadricNormals(quad, GLU_SMOOTH)
            gluQuadricTexture(quad, GL_TRUE)
            gluSphere(quad, self._ra, 50, 50)
        if self._st:
            glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, True)
        else:
            glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, False)
        glPopMatrix()

    def getMass(self):
        """Returns the Mass of the Astronomical Object"""
        return self._ma

    def getDensity(self):
        """Returns the Density of the Astronomical Object"""
        return self._de

    def getPosition(self):
        """Returns the Position of the Astronomical Object"""
        return self._po

    def getVelocity(self):
        """Returns the Velocity of the Astronomical Object"""
        return self._ve

    def getAngularPosition(self):
        """Returns the Angular Rotation of the Astronomical Object"""
        return self._ap

    def getAngularVelocity(self):
        """Returns the Angular Velocity of the Astronomical Object"""
        return self._av

    def getRadius(self):
        """Returns the Radius of the Astronomical Object"""
        return self._ra

    def getMomentum(self):
        """Returns the Momentum of the Astronomical Object"""
        return self._p

    def getMoment(self):
        """Returns the Moment of the Astronomical Object"""
        return self._mo

    def getExistence(self):
        """Returns Whether the Astronomical Object Exists"""
        return self._e

    def getTexture(self):
        """Returns The Texture ID of the Astronomical Object"""
        return self._tex

    def setMass(self, mass):
        """Sets the Mass of the Astronomical Object"""
        self._ma = mass

    def setDensity(self, density):
        """Sets the Density of the Astronomical Object"""
        self._de = density

    def setPosition(self, position):
        """Sets the Position of the Astronomical Object"""
        self._po = position

    def setVelocity(self, velocity):
        """Sets the Velocity of the Astronomical Object"""
        self._ve = velocity

    def setAngularPosition(self, angle):
        """Sets the Angular Rotation of the Astronomical Object"""
        self._ap = angle

    def setAngularVelocity(self, angular_velocity):
        """Sets the Angular Velocity of the Astronomical Object"""
        self._av = angular_velocity

    def setRadius(self, radius):
        """Sets the Radius of the Astronomical Object"""
        self._ra = radius

    def setMomentum(self, momentum):
        """Sets the Momentum of the Astronomical Object"""
        self._p = momentum

    def setExistence(self, exists):
        """Sets the Existence of the Astronomical Object"""
        self._e = exists

    def setTexture(self, texture):
        """Sets the Texture of the Astronomical Object"""
        self._tex = texture