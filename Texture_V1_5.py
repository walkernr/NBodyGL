# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 02:03:52 2013

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
from PIL import Image
import os
import dircache
import time

def texJPG(filename):
    img = Image.open(filename)
    img_data = img.tostring()
    ID = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glBindTexture(GL_TEXTURE_2D, ID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, img.size[0], img.size[1], GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return ID

def textureList():
    print 'TEXTURES LOADING' + '\n' + '================'
    textures = []
    images = dircache.listdir('jpgs')
    i = 0
    for filename in images:
        texture = texJPG(os.path.join('jpgs', filename))
        textures.append(texture)
        sys.stdout.write('\r')
        sys.stdout.write("[%-26s] %d%%" % ('=='*i, (100/13.)*i))
        sys.stdout.flush()
        i += 1
    sys.stdout.write('\n')
    return textures