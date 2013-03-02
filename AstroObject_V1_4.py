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

class AstroObject:
    """A Class for Creating and Manipulating an Astronomical Object"""

    def __init__(self, mass = .1, density = .2, position = [0.0, 0.0, 0.0], velocity = [0.0, 0.0, 0.0], angular_position = 0.0, angular_velocity = 2, ambient = [1.0, 1.0, 1.0, 1.0], diffuse = [1.0, 1.0, 1.0, 1.0], specular = [1.0, 1.0, 1.0, 1.0], emissive = [0.0, 0.0, 0.0, 0.0], shininess = .5, exists = True):
        """Initializes Values of Astronomical Object"""
        self._ma = mass
        self._de = density
        self._po = array(position)
        self._ve = array(velocity)
        self._ap = angular_position
        self._av = angular_velocity
        self._am = array(ambient)
        self._di = array(diffuse)
        self._sp = array(specular)
        self._em = array(emissive)
        self._sh = shininess
        self._ra = sqrt(self._ma * 3.0 / 4.0 / self._de / pi)
        self._p = self._ma * self._ve
        self._mo = self._ma * self._po
        self._e = exists

    def updateAstro(self):
        """Updates the Astronomical Object and Draws It"""
        self._ra = sqrt(self._ma * 3.0 / 4.0 / self._de / pi)
        self._ve = self._p / self._ma
        self._mo = self._ma * self._po
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT, self._am)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self._di)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self._sp)
        glMaterialfv(GL_FRONT, GL_EMISSION, self._em)
        glMaterialf(GL_FRONT, GL_SHININESS, self._sh * 128.0)
        #glRotatef(self._ap + self._av, 0.0, 0.0, 1.0)
        self._ap = self._ap + self._av
        glTranslate(self._po[0], self._po[1], self._po[2])
        glutSolidSphere(self._ra, 50, 50)
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

    def getAmbientLight(self):
        """Returns the Ambient Lighting of the Astronomical Object"""
        return self._am

    def getDiffuseLight(self):
        """Returns the Diffuse Lighting of the Astronomical Object"""
        return self._di

    def getSpecularLight(self):
        """Returns the Specular Lighting of the Astronomical Object"""
        return self._sp

    def getEmissiveLight(self):
        """Returns the Emission of Light from the Astronomical Object"""
        return self._em

    def getShininess(self):
        """Returns the Shininess of the Astronomical Object"""
        return self._sh

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

    def setAmbientLight(self, ambient):
        """Sets the Ambient Light of the Astronomical Object"""
        self._am = ambient

    def setDiffuseLight(self, diffuse):
        """Sets the Diffuse Light of the Astronomical Object"""
        self._di = diffuse

    def setSpecularLight(self, specular):
        """Sets the Specular Light of the Astronomical Object"""
        self._sp = specular

    def setEmissiveLight(self, emissive):
        """Sets the Emission of Light from the Astronomical Object"""
        self._em = emissive

    def setShininess(self, shininess):
        """Sets the Shininess of the Astronomical Object"""
        self._sh = shininess

    def setMomentum(self, momentum):
        """Sets the Momentum of the Astronomical Object"""
        self._p = momentum

    def setExistence(self, exists):
        """Sets the Existence of the Astronomical Object"""
        self._e = exists