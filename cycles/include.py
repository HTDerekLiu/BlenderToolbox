import bpy, bmesh
import numpy as np

from utils.blenderInit import *
from utils.colorMap import *
from utils.drawPoints import *
from utils.invisibleGround import *
from utils.lookAt import *
from utils.readPLY import *
from utils.readOBJ import *
from utils.setCamera import *
from utils.setLight_sun import *
from utils.setLight_ambient import *
from utils.setMat_edge import *
from utils.setMat_singleColor import *
from utils.setMat_pointCloud import *
from utils.setMat_VColor import *
from utils.setMat_monotone import *
from utils.subdivision import *

derekBlue = (144.0/255, 210.0/255, 236.0/255, 0)
coralRed = (250.0/255, 114.0/255, 104.0/255, 0)
iglGreen = (153.0/255, 203.0/255, 67.0/255, 0)
royalBlue = (0/255, 35/255, 102/255, 0)

class discreteColor(object):
    def __init__(self, brightness = 0, pos1 = 0, pos2 = 0):
        self.brightness = brightness
        self.rampElement1_pos = pos1
        self.rampElement2_pos = pos2

class HSVColor(object):
    def __init__(self, \
    hue = 0.5, \
    saturation = 1.0, \
    brightness = 1.0,\
    RGBA = derekBlue):
        self.H = hue
        self.S = saturation
        self.V = brightness
        self.RGBA = RGBA