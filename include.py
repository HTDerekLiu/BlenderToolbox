import sys
sys.path.append('./utils')

from ambientOcclusion import *
from blenderInit import *
from drawPointCloud import *
from invisibleGround import *
from lookAt import *
from readPLY import *
from readOBJ import *
from setCamera import *
from setLight_sun import *
from setLight_ambient import *
from setMat_edge import *
from setMat_normal import *
from setMat_VColor import *
from subdivision import *

derekBlue = (144.0/255, 210.0/255, 236.0/255, 0)
coralRed = (250.0/255, 114.0/255, 104.0/255, 0)
iglGreen = (153.0/255, 203.0/255, 67.0/255, 0)