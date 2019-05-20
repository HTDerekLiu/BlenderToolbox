import bpy, bmesh
import numpy as np

from utils.initColorNode import *
from utils.blenderInit import *
from utils.colorMap import *
from utils.drawPoints import *
from utils.drawLines import *
from utils.drawVertexSubset import *
from utils.drawBoundaryLoop import *
from utils.edgeNormals import *
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
from utils.setMat_chrome import *
from utils.setMat_crackedCeramic import *
from utils.setMat_ceramic import *
from utils.setMat_edge import *
from utils.setMat_glass import *
from utils.setMat_singleColor import *
from utils.setMat_stone import *
from utils.setMat_transparent import *
from utils.setMat_texture import *
from utils.setMat_pointCloud import *
from utils.setMat_VColor import *
from utils.setMat_monotone import *
from utils.subdivision import *

derekBlue = (144.0/255, 210.0/255, 236.0/255, 1)
coralRed = (250.0/255, 114.0/255, 104.0/255, 1)
iglGreen = (153.0/255, 203.0/255, 67.0/255, 1)
royalBlue = (0/255, 35/255, 102/255, 1)
royalYellow = (250.0/255,218.0/255,94.0/255, 1)

# color palette for colr blindness (source: http://mkweb.bcgsc.ca/colorblind)
cb_black = (0/255.0, 0/255.0, 236/255.0, 1)
cb_orange = (230/255.0, 159/255.0, 0/255.0, 1)
cb_skyBlue = (86/255.0, 180/255.0, 233/255.0, 1)
cb_green = (0/255.0, 158/255.0, 115/255.0, 1)
cb_yellow = (240/255.0, 228/255.0, 66/255.0, 1)
cb_blue = (0/255.0, 114/255.0, 178/255.0, 1)
cb_vermillion = (213/255.0, 94/255.0, 0/255.0, 1)
cb_purple = (204/255.0, 121/255.0, 167/255.0, 1)

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
