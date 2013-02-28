# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 02:22:01 2013

@author: Nick Walker
"""

from AstroObject_V1_3 import *
from numpy import dot, array, pi, sin, cos, sqrt
from random import uniform, randint

def getVector(vector_a, vector_b):
    return array(vector_b) - array(vector_a)

def getVectorMagnitude(vector_a, vector_b):
    return sqrt((vector_b[0] - vector_a[0])**2 + (vector_b[1] - vector_a[1])**2 + (vector_b[2] - vector_a[2])**2)

def rotationMatrix(axis,theta):
    axis = axis / sqrt(dot(axis,axis))
    a = cos(theta / 2)
    b,c,d = - axis * sin(theta/2)
    return array([[a * a + b * b - c * c - d * d, 2 * (b * c - a * d), 2 * (b * d + a * c)], [2 * (b * c + a * d), a * a + c * c - b * b - d * d, 2 * (c * d - a * b)], [2 * (b * d - a * c), 2 * (c * d + a * b), a * a + d * d - b * b - c * c]])

def getCentripetalVelocity(object_a, object_b):
    g = 1e-4
    m = object_a.getMass()
    rv = getRelativeRadius(object_b, object_a)
    r = getRelativeRadiusMagnitude(object_b, object_a)
    a = array([0.0, 0.0, 1.0])
    v = sqrt(g * m / r) * rv / r
    return dot(rotationMatrix(a, pi / 2), v)

def getTotalMass(AstroObjects):
    mass = 0.0
    for object_a in AstroObjects:
        mass = mass + object_a.getmass()
    return mass

def getCenterOfMass(AstroObjects):
    moment = 0.0
    for object_a in AstroObjects:
        moment = moment + object_a.getMoment()
    mass = getTotalMass(AstroObjects)
    return moment/mass

def getCenterofMassVelocity(AstroObjects):
    momentum = 0.0
    for object_a in AstroObjects:
        momentum = momentum + object_a.getMomentum()
    mass = getTotalMass(AstroObjects)
    return momentum/mass

def getRelativeRadiusMagnitude(object_a, object_b):
    return sqrt((object_b.getPosition()[0] - object_a.getPosition()[0])**2 + (object_b.getPosition()[1] - object_a.getPosition()[1])**2 + (object_b.getPosition()[2] - object_a.getPosition()[2])**2)

def getRelativeRadiiMagnitudes(AstroObjects):
    radii = []
    for object_a in AstroObjects:
        oradii = []
        for object_b in AstroObjects:
            oradii.append(getRelativeRadiusMagnitude(object_a, object_b))
        radii.append(oradii)
    return radii

def getRelativeRadius(object_a, object_b):
    return object_b.getPosition() - object_a.getPosition()

def getRelativeRadii(AstroObjects):
    radii = []
    for object_a in AstroObjects:
        oradii = []
        for object_b in AstroObjects:
            oradii.append(getRelativeRadius(object_a, object_b))
        radii.append(oradii)
    return radii

def getCollisionList(AstroObjects):
    collisionlist = []
    for object_a in AstroObjects:
        for object_b in AstroObjects:
            if getRelativeRadiusMagnitude(object_a, object_b) <= object_a.getRadius() + object_b.getRadius() and object_a != object_b and [object_b, object_a] not in collisionlist:
                object_a.setExistence(False)
                object_b.setExistence(False)
                collisionlist.append([object_a, object_b])
    return collisionlist

def updateCollisions(AstroObjects):
    collisions = getCollisionList(AstroObjects)
    objects = []
    for collision in collisions:
        modified_mass = collision[0].getMass() + collision[1].getMass()
        modified_velocity = (collision[0].getMomentum() + collision[1].getMomentum()) / modified_mass
        modified_position = (collision[0].getMoment() + collision[1].getMoment()) / modified_mass
        modified_density = (collision[0].getMass() * collision[0].getDensity() + collision[1].getMass() * collision[1].getDensity()) / modified_mass
        modified_angular_position = (collision[0].getMass() * collision[0].getAngularPosition() + collision[1].getMass() * collision[1].getAngularPosition()) / modified_mass
        modified_angular_velocity = (collision[0].getMass() * collision[0].getAngularVelocity() + collision[1].getMass() * collision[1].getAngularVelocity()) / modified_mass
        modified_ambient = (collision[0].getMass() * collision[0].getAmbientLight() + collision[1].getMass() * collision[1].getAmbientLight()) / modified_mass
        modified_diffuse = (collision[0].getMass() * collision[0].getDiffuseLight() + collision[1].getMass() * collision[1].getDiffuseLight()) / modified_mass
        modified_specular = (collision[0].getMass() * collision[0].getSpecularLight() + collision[1].getMass() * collision[1].getSpecularLight()) / modified_mass
        modified_shininess = (collision[0].getMass() * collision[0].getShininess() + collision[1].getMass() * collision[1].getShininess()) / modified_mass
        b_mass = max(collision[0].getMass(), collision[1].getMass())
        m_mass = min(collision[0].getMass(), collision[1].getMass())
        if b_mass / m_mass < 2.0:
            modified_radius = sqrt(modified_mass * 3.0 / 4.0 / modified_density / pi)
            modified_momentum = modified_velocity * modified_mass
            p = modified_momentum
            m = modified_mass
            momenta = []
            masses = []
            for n in range(randint(0, 5)):
                mass = uniform(0, m / 10.0)
                masses.append(mass)
                m = m - mass
                momentum = array([uniform(-p[0], p[0]), uniform(-p[1], p[1]), uniform(-p[2], p[2])])
                momenta.append(momentum)
                p = p - momentum
            masses.append(m)
            momenta.append(p)
            for n in range(len(masses)):
                n_object = AstroObject(mass = masses[n], density = 1.5 * modified_density, position = modified_position, velocity = momenta[n] / modified_mass, angular_position = modified_angular_position, angular_velocity = modified_angular_velocity, ambient = modified_ambient, diffuse = modified_diffuse, specular = modified_specular, shininess = modified_shininess)
                n_object.setPosition(n_object.getPosition() + modified_radius * n_object.getVelocity() / getVectorMagnitude(n_object.getVelocity(), array([0.0, 0.0, 0.0])))
                AstroObjects.append(n_object)
        else:
            modified_object = AstroObject(mass = modified_mass, density = modified_density, position = modified_position, velocity = modified_velocity, angular_position = modified_angular_position, angular_velocity = modified_angular_velocity, ambient = modified_ambient, diffuse = modified_diffuse, specular = modified_specular, shininess = modified_shininess)
            AstroObjects.append(modified_object)

    for object_a in AstroObjects:
        if object_a.getExistence() != False:
            objects.append(object_a)
    return objects

def getGravitationalForce(object_a, object_b):
    g = 1e-4
    uv = getRelativeRadius(object_a, object_b) / getRelativeRadiusMagnitude(object_a, object_b)
    force = g * object_a.getMass() * object_b.getMass() * uv / getRelativeRadiusMagnitude(object_a, object_b)**2
    return force

def getGravitationalForces(AstroObjects):
    forces = []
    for object_a in AstroObjects:
        oforces = []
        for object_b in AstroObjects:
            if object_a == object_b:
                oforces.append(array([0.0, 0.0, 0.0]))
            else:
                oforces.append(getGravitationalForce(object_a, object_b))
        forces.append(array(oforces))
    return forces

def deleteObjects(AstroObjects):
    objects = []
    for object_a in AstroObjects:
        if getVectorMagnitude(object_a.getPosition(), array([0.0, 0.0, 0.0])) < 10.0:
            objects.append(object_a)
    return objects

def updateMomenta(AstroObjects):
    dt = .5
    forces = getGravitationalForces(AstroObjects)
    momenta = []
    for n in range(len(forces)):
        momenta.append(0.0)
        for m in range (len(forces)):
            momenta[n] = momenta[n] + forces[n][m]
    for n in range(len(AstroObjects)):
        momentum = AstroObjects[n].getMomentum() + momenta[n] * dt
        AstroObjects[n].setMomentum(momentum)

def updatePositions(AstroObjects):
    dt = .5
    updateMomenta(AstroObjects)
    for object_a in AstroObjects:
        position = object_a.getPosition() + (object_a.getMomentum() / object_a.getMass()) * dt
        object_a.setPosition(position)