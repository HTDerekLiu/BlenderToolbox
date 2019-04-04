import bpy, bmesh
import numpy as np

from utils.initColorNode import *
from utils.blenderInit import *
from utils.colorMap import *
from utils.drawPoints import *
from utils.invisibleGround import *
from utils.lookAt import *
from utils.loadShader import *
from utils.readPLY import *
from utils.readOBJ import *
from utils.setCamera import *
from utils.setLight_sun import *
from utils.setLight_ambient import *
from utils.setMat_amber import *
from utils.setMat_carPaint import *
from utils.setMat_crackedCeramic import *
from utils.setMat_ceramic import *
from utils.setMat_edge import *
from utils.setMat_singleColor import *
from utils.setMat_pointCloud import *
from utils.setMat_VColor import *
from utils.setMat_monotone import *
from utils.subdivision import *

derekBlue = (144.0/255, 210.0/255, 236.0/255, 1)
coralRed = (250.0/255, 114.0/255, 104.0/255, 1)
iglGreen = (153.0/255, 203.0/255, 67.0/255, 1)
royalBlue = (0/255, 35/255, 102/255, 1)

class discreteColor(object):
    def __init__(self, brightness = 0, pos1 = 0, pos2 = 0):
        self.brightness = brightness
        self.rampElement1_pos = pos1
        self.rampElement2_pos = pos2

class colorObj(object):
    def __init__(self, RGBA = derekBlue, \
    H = 0.5, S = 1.0, V = 1.0,\
    B = 0.0, C = 0.0):
        self.H = H # hue
        self.S = S # saturation
        self.V = V # value
        self.RGBA = RGBA
        self.B = B # birghtness
        self.C = C # contrast
