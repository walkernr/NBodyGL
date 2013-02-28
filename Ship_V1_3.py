# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 18:15:13 2013

@author: Nick Walker
"""

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Newton_V1_3 import *
from numpy import dot, array, pi

class Ship:
    """A Class for Managing a Ship Flying through the System"""

    def __init__(self, camera = [10.0, 0.0, 0.0], target = [0.0, 0.0, 0.0], transverse = [0.0, 1.0, 0.0], frange = 10000.0):
        """Takes Camera Position, Target Position, Transverse Axis, and Maximum Range as Inputs"""
        self._camera = array(camera)
        self._target = array(target)
        self._transverse = array(transverse)
        self._frange = frange

    def getCamera(self):
        """Returns the Position of the Camera"""
        return self._camera

    def getTarget(self):
        """Returns the Position of the Target"""
        return self._target

    def getTransverse(self):
        """Returns the Transverse Axis"""
        return self._transverse

    def getFRange(self):
        """Returns the Maximum Range"""
        return self._frange

    def setCamera(self, camera):
        """Sets the Camera Position"""
        self._camera = camera

    def setTarget(self, target):
        """Sets the Target Position"""
        self._target = Target

    def setTransverse(self, transverse):
        """Sets the Transverse Axis"""
        self._transverse = transverse

    def setFRange(self, frange):
        """Sets the Maximum Range"""
        self._frange = frange

    def zoomIn(self):
        """Zooms in the Camera"""
        self._camera = array(self._camera) * .95
        glutPostRedisplay()

    def zoomOut(self):
        """Zooms out the Camera"""
        self._camera = array(self._camera) * 1.05
        glutPostRedisplay()

    def rotateUp(self):
        """Rotates the Camera Up"""
        self._target = array([0.0, 0.0, 0.0])
        self._camera = dot(rotationMatrix(array([0.0, 1.0, 0.0]), pi / 180), array(self._camera))
        glutPostRedisplay()

    def rotateDown(self):
        """Rotates the Camera Down"""
        self._target = array([0.0, 0.0, 0.0])
        self._camera = dot(rotationMatrix(array([0.0, 1.0, 0.0]), -pi / 180), array(self._camera))
        glutPostRedisplay()

    def rotateLeft(self):
        """Rotates the Camera Left"""
        self._target = array([0.0, 0.0, 0.0])
        self._camera = dot(rotationMatrix(array([0.0, 0.0, 1.0]), -pi / 180), array(self._camera))
        self._transverse = dot(rotationMatrix(array([0.0, 0.0, 1.0]), -pi / 180), array(self._transverse))
        glutPostRedisplay()

    def rotateRight(self):
        """Rotates the Camera Right"""
        self._target = array([0.0, 0.0, 0.0])
        self._camera = dot(rotationMatrix(array([0.0, 0.0, 1.0]), pi / 180), array(self._camera))
        self._transverse = dot(rotationMatrix(array([0.0, 0.0, 1.0]), pi / 180), array(self._transverse))
        glutPostRedisplay()

    def forward(self):
        """Moves the Camera Forward"""
        self._target = self._frange * getVector(self._camera, self._target)/getVectorMagnitude(self._camera, self._target)
        self._camera = array(self._camera) + .05 * getVector(self._camera, self._target)/getVectorMagnitude(self._camera, self._target)
        glutPostRedisplay()

    def backward(self):
        """Moves the Camera Backward"""
        self._target = self._frange * getVector(self._camera, self._target)/getVectorMagnitude(self._camera, self._target)
        self._camera = array(self._camera) - .05 * getVector(self._camera, self._target)/getVectorMagnitude(self._camera, self._target)
        glutPostRedisplay()

    def up(self):
        """Moves the Camera Facing Up"""
        self._target = self._frange * getVector(self._camera, self._target)/getVectorMagnitude(self._camera, self._target)
        self._target = dot(rotationMatrix(self._transverse, -2 * pi / 180), array(self._target))
        glutPostRedisplay()

    def down(self):
        """Moves the Camera Facing Down"""
        self._target = self._frange * getVector(self._camera, self._target)/getVectorMagnitude(self._camera, self._target)
        self._target = dot(rotationMatrix(self._transverse, 2 * pi / 180), array(self._target))
        glutPostRedisplay()

    def left(self):
        """Moves the Camera Facing Left"""
        self._target = self._frange * getVector(self._camera, self._target)/getVectorMagnitude(self._camera, self._target)
        self._target = dot(rotationMatrix(array([0.0, 0.0, 1.0]), -2 * pi / 180), array(self._target))
        self._transverse = dot(rotationMatrix(array([0.0, 0.0, 1.0]), -2 * pi / 180), array(self._transverse))
        glutPostRedisplay()

    def right(self):
        """Moves the Camera Facing Right"""
        self._target = self._frange * getVector(self._camera, self._target)/getVectorMagnitude(self._camera, self._target)
        self._target = dot(rotationMatrix(array([0.0, 0.0, 1.0]), 2 * pi / 180), array(self._target))
        self._transverse = dot(rotationMatrix(array([0.0, 0.0, 1.0]), 2 * pi / 180), array(self._transverse))
        glutPostRedisplay()

    def stop(self):
        """Stops Camera Motion"""
        self._target = self._frange * getVector(self._camera, self._target)/getVectorMagnitude(self._camera, self._target)
        self._camera = array(self._camera)
        glutPostRedisplay()

    def facing(self, x, y, w, h):
        """Changes the Facing of the Camera Based on the Position of the Mouse"""
        ax = 0
        ay = 0
        if x > 2 * w / 3.0:
            ax = 1
        if x < 1 * w / 3.0:
            ax = -1
        if y > 2 * h / 3.0:
            ay = 1
        if y < 1 * h / 3.0:
            ay = -1
        self._target = self._frange * getVector(self._camera, self._target)/getVectorMagnitude(self._camera, self._target)
        self._target = dot(rotationMatrix(array([0.0, 0.0, 1.0]), ax * pi / 180), array(self._target))
        self._transverse = dot(rotationMatrix(array([0.0, 0.0, 1.0]), ax * pi / 180), array(self._transverse))
        self._target = dot(rotationMatrix(self._transverse, ay * pi / 180), array(self._target))