# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 02:22:01 2013

@author: Nick Walker

This program simulates the motion of an N-Body system and allows for traversal with keyboard and mouse input

Copyright (c) 2013 Nicholas Walker

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from AstroObject_V1_5 import *
from numpy import *
from random import uniform, randint

def getVector(vector_a, vector_b):
    #the difference between two vectors
    return array(vector_b) - array(vector_a)

def getVectorMagnitude(vector_a, vector_b):
    # r = sqrt(x^2 +y^2 + z^2)
    return sqrt((vector_b[0] - vector_a[0])**2 + (vector_b[1] - vector_a[1])**2 + (vector_b[2] - vector_a[2])**2)

def rotationMatrix(axis,theta):
    #the euler-rodrigues formula
    axis = axis / sqrt(dot(axis,axis))
    a = cos(theta / 2)
    b,c,d = - axis * sin(theta/2)
    return array([[a * a + b * b - c * c - d * d, 2 * (b * c - a * d), 2 * (b * d + a * c)], [2 * (b * c + a * d), a * a + c * c - b * b - d * d, 2 * (c * d - a * b)], [2 * (b * d - a * c), 2 * (c * d + a * b), a * a + d * d - b * b - c * c]])

def getCentripetalVelocity(object_a, object_b):
    #this calculates the centripetal velocity (f = mv^2/r)
    g = 1e-4
    m = object_a.getMass()
    rv = getRelativeRadius(object_a, object_b)
    r = getRelativeRadiusMagnitude(object_a, object_b)
    a = array([0.0, 0.0, 1.0])
    v = sqrt(g * m / r) * rv / r
    return dot(rotationMatrix(a, pi / 2), v)

def getTotalMass(AstroObjects):
    #this sums the masses in the system
    mass = 0.0
    for object_a in AstroObjects:
        mass = mass + object_a.getmass()
    return mass

def getCenterOfMass(AstroObjects):
    #this finds the center of mass by summing the moments and dividing by the total mass
    moment = zeroes(1,3)
    for object_a in AstroObjects:
        moment = moment + object_a.getMoment()
    mass = getTotalMass(AstroObjects)
    return moment/mass

def getCenterofMassVelocity(AstroObjects):
    #this finds the velcoity of the center of mass by summing the momenta then dividing by the total mass
    momentum = zeroes(1,3)
    for object_a in AstroObjects:
        momentum = momentum + object_a.getMomentum()
    mass = getTotalMass(AstroObjects)
    return momentum/mass

def getRelativeRadiusMagnitude(object_a, object_b):
    # this finds the magnitude of the distance between two objects
    return sqrt((object_b.getPosition()[0] - object_a.getPosition()[0])**2 + (object_b.getPosition()[1] - object_a.getPosition()[1])**2 + (object_b.getPosition()[2] - object_a.getPosition()[2])**2)

def getRelativeRadiiMagnitudes(AstroObjects):
    #this constructs a matrix of relative distances between objects
    radii = []
    for object_a in AstroObjects:
        oradii = []
        for object_b in AstroObjects:
            oradii.append(getRelativeRadiusMagnitude(object_a, object_b))
        radii.append(oradii)
    return radii

def getRelativeRadius(object_a, object_b):
    #this calculates a position vector between two objects
    return object_b.getPosition() - object_a.getPosition()

def deleteObjects(AstroObjects, maxr):
    #this deletes objects that stray too far from the system
    objects = []
    for object_a in AstroObjects:
        if getVectorMagnitude(object_a.getPosition(), array([0.0, 0.0, 0.0])) < maxr:
            objects.append(object_a)
    return objects

def getAllMasses(AstroObjects):
    #this constructs a matrix of the masses in the system
    masses = zeros((len(AstroObjects), 1), dtype = float)
    for n in range(len(AstroObjects)):
        masses[n] = AstroObjects[n].getMass()
    return masses

def getAllRelativeRadii(AstroObjects):
    #this constructs a matrix of the relative position vectors between objects
    radii = zeros((len(AstroObjects), 3), dtype = float)
    for n in range(len(AstroObjects)):
        radii[n] = AstroObjects[n].getPosition()
    rmatrix = radii - radii[:, newaxis]
    for n in range(len(AstroObjects)):
        #self displacement is practically infinity
        rmatrix[n][n] = [1e20, 1e20, 1e20]
    return rmatrix

def getAllRelativeRadiiMagnitudes(AstroObjects):
    #this constructs a matrix of the magnitudes of the distances between objects
    return sqrt(sum(square(getAllRelativeRadii(AstroObjects)), -1))

def getAllRelativeForces(AstroObjects):
    g = 1e-4
    mass = getAllMasses(AstroObjects)
    radii = getAllRelativeRadii(AstroObjects)
    radiimag = getAllRelativeRadiiMagnitudes(AstroObjects)
    fmatrix = g * mass * mass[:, newaxis] * radii / radiimag[:, :, newaxis] ** 3
    for n in range(len(AstroObjects)):
        fmatrix[n][n] = 0.0
    return fmatrix

def getCollisions(AstroObjects, teapots):
    objects = []
    collisionlist = zeros((len(AstroObjects), len(AstroObjects)), dtype = float)
    for m in range(len(AstroObjects)):
        if sum(collisionlist[m], 0) == 0:
            for n in range(len(AstroObjects)):
                if getRelativeRadiusMagnitude(AstroObjects[m], AstroObjects[n]) <= AstroObjects[m].getRadius() + AstroObjects[n].getRadius() and AstroObjects[m] != AstroObjects[n]:
                    collisionlist[n][m] = 1
    new_objects = []
    for m in range(len(AstroObjects)):
        masses = zeros((len(AstroObjects), 1), dtype = float)
        velocities = zeros((len(AstroObjects), 3), dtype = float)
        positions = zeros((len(AstroObjects), 3), dtype = float)
        densities = zeros((len(AstroObjects), 1), dtype = float)
        angularpositions = zeros((len(AstroObjects), 1), dtype = float)
        angularvelocities = zeros((len(AstroObjects), 1), dtype = float)
        counter = 0
        for n in range(len(AstroObjects)):
            if collisionlist[m][n] == 1:
                counter = counter + 1
                masses[n] = AstroObjects[n].getMass()
                velocities[n] = AstroObjects[n].getVelocity()
                positions[n] = AstroObjects[n].getPosition()
                densities[n] = AstroObjects[n].getDensity()
                angularpositions[n] = AstroObjects[n].getAngularPosition()
                angularvelocities[n] = AstroObjects[n].getAngularVelocity()
                AstroObjects[n].setExistence(False)
        if counter > 0:
            modified_mass = sum(masses, 0) + AstroObjects[m].getMass()
            modified_velocity = (sum(masses * velocities, 0) + AstroObjects[m].getMass() * AstroObjects[m].getVelocity()) / modified_mass
            modified_position = (sum(masses * positions, 0) + AstroObjects[m].getMass() * AstroObjects[m].getPosition()) / modified_mass
            modified_density = (sum(masses * densities, 0) + AstroObjects[m].getMass() * AstroObjects[m].getDensity()) / modified_mass
            modified_angular_position = (sum(masses * angularpositions, 0) + AstroObjects[m].getMass() * AstroObjects[m].getAngularPosition()) / modified_mass
            modified_angular_velocity = (sum(masses * angularvelocities, 0) + AstroObjects[m].getMass() * AstroObjects[m].getAngularVelocity()) / modified_mass
            modified_momentum = modified_mass * modified_velocity
            greatest_mass = max(max(masses), AstroObjects[m].getMass())
            for n in range(len(AstroObjects)):
                if AstroObjects[n].getMass() == greatest_mass:
                    modified_texture = AstroObjects[n].getTexture()
            #modified_texture = AstroObjects[m].getTexture()
            if getVectorMagnitude(modified_momentum, array([0.0, 0.0, 0.0])) > 0.0:
                modified_energy = zeros((1,3))
                modified_energy[0] = modified_momentum ** 3 / 2 / modified_mass / getVectorMagnitude(modified_momentum, array([0.0, 0.0, 0.0]))
            else:
                modified_energy = zeros((1,3))
            AstroObjects[m].setExistence(False)
            comparison = sort(masses, axis = None)
            comparison[0] = AstroObjects[m].getMass()
            comparison = sort(comparison)
            if comparison[len(comparison) -1] / comparison[len(comparison) - 2] < 10:
                modified_radius = sqrt(modified_mass * 3.0 / 4.0 / modified_density / pi)
                e = modified_energy
                ma = modified_mass
                momenta = zeros((6, 3), dtype = float)
                masses = zeros((6, 1), dtype = float)
                for n in range(randint(2, 5)):
                    mass = uniform(0.0, ma / 20.0)
                    masses[n] = mass
                    ma = ma - mass
                    energy = array([uniform(-1e-6, 1e-6), uniform(-1e-6, 1e-6), 0.0])
                    u = energy / getVectorMagnitude(energy, array([0.0, 0.0, 0.0]))
                    momentum = sqrt(2 * mass * energy * u) * u
                    momenta[n] = momentum
                    e = e - energy
                masses[5] = ma
                unitv = e[0] / getVectorMagnitude(e[0], array([0.0, 0.0, 0.0]))
                momenta[5] = sqrt(2 * ma * abs(e[0])) * unitv
                for n in range(6):
                    if masses[n] > 0.0:
                        n_object = AstroObject(mass = masses[n], density = modified_density, position = modified_position, velocity = momenta[n] / modified_mass, angular_position = modified_angular_position, angular_velocity = modified_angular_velocity, texture = modified_texture, teapot = teapots)
                        if getVectorMagnitude(n_object.getVelocity(), array([0.0, 0.0, 0.0])) > 0.0:
                            n_object.setPosition(n_object.getPosition() + modified_radius * n_object.getVelocity() / getVectorMagnitude(n_object.getVelocity(), array([0.0, 0.0, 0.0])))
                        new_objects.append(n_object)
            else:
                modified_object = AstroObject(mass = modified_mass, density = modified_density, position = modified_position, velocity = modified_velocity, angular_position = modified_angular_position, angular_velocity = modified_angular_velocity, texture = modified_texture, teapot = teapots)
                new_objects.append(modified_object)
    for object_a in new_objects:
        objects.append(object_a)
    for object_a in AstroObjects:
        if object_a.getExistence() != False:
            objects.append(object_a)
    return objects


def calculateKinematics(AstroObjects):
    dt = .5
    momenta = zeros((len(AstroObjects), 3), dtype = float)
    positions = zeros((len(AstroObjects), 3), dtype = float)
    for n in range(len(AstroObjects)):
        momenta[n] = AstroObjects[n].getMomentum()
        positions[n] = AstroObjects[n].getPosition()
    momenta = momenta + sum(getAllRelativeForces(AstroObjects), 1) * dt
    positions = positions + (momenta / getAllMasses(AstroObjects)) * dt
    return [momenta, positions]

def update(AstroObjects):
    kinematics = calculateKinematics(AstroObjects)
    for n in range(len(AstroObjects)):
        AstroObjects[n].setMomentum(kinematics[0][n])
        AstroObjects[n].setPosition(kinematics[1][n])