from distutils.core import setup
import py2exe

setup(windows=['NBody_V1_0.py'],
      options={
          "py2exe": {
              "includes": ["ctypes", "logging"],
              "excludes": ["OpenGL"],
              }
          }
      )