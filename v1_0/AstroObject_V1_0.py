# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 01:41:28 2013

@author: Nick Walker
"""

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import array, pi, sqrt

class AstroObject:
    """A Class for Creating and Manipulating an Astrological Object"""

    def __init__(self, mass = 1.0, density = 1.0, position = [0.0, 0.0, 0.0], velocity = [0.0, 0.0, 0.0], angular_position = 0.0, angular_velocity = 2, ambient = [1.0, 1.0, 1.0, 1.0], diffuse = [1.0, 1.0, 1.0, 1.0], specular = [1.0, 1.0, 1.0, 1.0], shininess = .5, exists = True):
        """Initializes Values of Astrological Object"""
        self._ma = mass
        self._de = density
        self._po = array(position)
        self._ve = array(velocity)
        self._ap = angular_position
        self._av = angular_velocity
        self._am = array(ambient)
        self._di = array(diffuse)
        self._sp = array(specular)
        self._sh = shininess
        self._ra = sqrt(self._ma * 3.0 / 4.0 / self._de / pi)
        self._p = self._ma * self._ve
        self._mo = self._ma * self._po
        self._e = exists

    def updateAstro(self):
        """Updates the Astrological Object and Draws It"""
        self._ra = sqrt(self._ma * 3.0 / 4.0 / self._de / pi)
        self._ve = self._p / self._ma
        self._mo = self._ma * self._po
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT, self._am)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self._di)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self._sp)
        glMaterialf(GL_FRONT, GL_SHININESS, self._sh * 128.0)
        #glRotatef(self._ap + self._av, 0.0, 0.0, 1.0)
        self._ap = self._ap + self._av
        glTranslate(self._po[0], self._po[1], self._po[2])
        glutSolidSphere(self._ra, 50, 50)
        glPopMatrix()

    def getMass(self):
        """Returns the Mass of the Astrological Object"""
        return self._ma

    def getDensity(self):
        """Returns the Density of the Astrological Object"""
        return self._de

    def getPosition(self):
        """Returns the Position of the Astrological Object"""
        return self._po

    def getVelocity(self):
        """Returns the Velocity of the Astrological Object"""
        return self._ve

    def getAngularPosition(self):
        """Returns the Angular Rotation of the Astrological Object"""
        return self._ap

    def getAngularVelocity(self):
        """Returns the Angular Velocity of the Astrological Object"""
        return self._av

    def getAmbientLight(self):
        """Returns the Ambient Lighting of the Astrological Object"""
        return self._am

    def getDiffuseLight(self):
        """Returns the Diffuse Lighting of the Astrological Object"""
        return self._di

    def getSpecularLight(self):
        """Returns the Specular Lighting of the Astrological Object"""
        return self._sp

    def getShininess(self):
        """Returns the Shininess of the Astrological Object"""
        return self._sh

    def getRadius(self):
        """Returns the Radius of the Astrological Object"""
        return self._ra

    def getMomentum(self):
        """Returns the Momentum of the Astrological Object"""
        return self._p

    def getMoment(self):
        """Returns the Moment of the Astrological Object"""
        return self._mo

    def getExistence(self):
        """Returns Whether the Astrological Object Exists"""
        return self._e

    def setMass(self, mass):
        """Sets the Mass of the Astrological Object"""
        self._ma = mass

    def setDensity(self, density):
        """Sets the Density of the Astrological Object"""
        self._de = density

    def setPosition(self, position):
        """Sets the Position of the Astrological Object"""
        self._po = position

    def setVelocity(self, velocity):
        """Sets the Velocity of the Astrological Object"""
        self._ve = velocity

    def setAngularPosition(self, angle):
        """Sets the Angular Rotation of the Astrological Object"""
        self._ap = angle

    def setAngularVelocity(self, angular_velocity):
        """Sets the Angular Velocity of the Astrological Object"""
        self._av = angular_velocity

    def setAmbientLight(self, ambient):
        """Sets the Ambient Light of the Astrological Object"""
        self._am = ambient

    def setDiffuseLight(self, diffuse):
        """Sets the Diffuse Light of the Astrological Object"""
        self._di = diffuse

    def setSpecularLight(self, specular):
        """Sets the Specular Light of the Astrological Object"""
        self._sp = specular

    def setShininess(self, shininess):
        """Sets the Shininess of the Astrological Object"""
        self._sh = shininess

    def setMomentum(self, momentum):
        """Sets the Momentum of the Astrological Object"""
        self._p = momentum

    def setExistence(self, exists):
        """Sets the Existence of the Astrological Object"""
        self._e = exists