# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 18:15:13 2013

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
from Newton_V1_5 import *
from numpy import *

class Ship:
    """A Class for Managing a Ship Flying through the System"""

    def __init__(self, camera = [10.0, 0.0, 0.0], target = [0.0, 0.0, 0.0], up = [0.0, 0.0, 1.0]):
        """Takes Camera Position, Target Position, Transverse Axis, and Maximum Range as Inputs"""
        self._camera = array(camera)
        self._target = array(target)
        self._up = array(up)
        self._fv = (array(target) - array(camera)) / getVectorMagnitude(array(target), array(camera))
        self._transverse = cross(self._up, self._fv)

    def calcTargetVector(self):
        """Calculates the location of the Target point"""
        self._target = self._camera + self._fv

    def calcUpVector(self):
        """Calculates the unit vector of the transverse vector of the Camera"""
        self._up = cross(self._transverse, self._fv)

    def calcTransverseVector(self):
        """Calculates the unit vector of the transverse vector of the Camera"""
        self._transverse = cross(self._up, self._fv)

    def getCamera(self):
        """Returns the Position of the Camera"""
        return self._camera

    def getTarget(self):
        """Returns the Position of the Target"""
        return self._target

    def getUp(self):
        """Returns the Position of the Up vector"""
        return self._up

    def getTransverse(self):
        """Returns the Transverse Axis"""
        return self._transverse

    def getFacingVector(self):
        """Returns the unit vector of the Camera facing"""
        return self._fv

    def setCamera(self, camera):
        """Sets the Camera Position"""
        self._camera = camera

    def setTarget(self, target):
        """Sets the Target Position"""
        self._target = Target

    def forward(self):
        """Moves the Camera Forward"""
        step = .05 * self._fv
        self._target = self._target + step
        self._camera = self._camera + step
        glutPostRedisplay()

    def backward(self):
        """Moves the Camera Backward"""
        step = .05 * self._fv
        self._target = self._target - step
        self._camera = self._camera - step
        glutPostRedisplay()

    def up(self):
        """Moves the Camera Facing Up"""
        self._fv = dot(rotationMatrix(self._transverse, -2 * pi / 180.), array(self._fv))
        self.calcTargetVector()
        #self.calcUpVector()
        glutPostRedisplay()

    def down(self):
        """Moves the Camera Facing Down"""
        self._fv = dot(rotationMatrix(self._transverse, 2 * pi / 180.), array(self._fv))
        self.calcTargetVector()
        #self.calcUpVector()
        glutPostRedisplay()

    def left(self):
        """Moves the Camera Facing Left"""
        self._fv = dot(rotationMatrix(self._up, -2 * pi / 180.), array(self._fv))
        self._target = self._camera + self._fv
        self.calcTransverseVector()
        glutPostRedisplay()

    def right(self):
        """Moves the Camera Facing Right"""
        self._fv = dot(rotationMatrix(self._up, 2 * pi / 180.), array(self._fv))
        self._target = self._camera + self._fv
        self.calcTransverseVector()
        glutPostRedisplay()

    def facing(self, x, y, w, h):
        """Changes the Facing of the Camera Based on the Position of the Mouse"""
        ax = 0.0
        ay = 0.0
        if x > 2 * w / 3.0:
            ax = (x - w / 2.0) / (w / 2.0)
        if x < 1 * w / 3.0:
            ax = - (w / 2.0 - x) / (w / 2.0)
        if y > 2 * h / 3.0:
            ay = (y - h / 2.0) / (h / 2.0)
        if y < 1 * h / 3.0:
            ay = - (h / 2.0 - y) / (h / 2.0)
        self._fv = dot(rotationMatrix(self._up, ax * pi / 180.), array(self._fv))
        self._fv = dot(rotationMatrix(self._transverse, ay * pi / 180.), array(self._fv))
        self._target = self._camera + self._fv
        self.calcTransverseVector()
        glutPostRedisplay()