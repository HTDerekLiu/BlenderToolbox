import sys
sys.path.append('/Users/hsuehtil/Dropbox/BlenderToolbox/') # change this to your path to “path/to/BlenderToolbox/"
import BlenderToolBox as bt
import os, bpy, bmesh
import numpy as np
cwd = os.getcwd()

outputPath = os.path.join(cwd, './template_pointCloud_numpy.png') # make it abs path for windows

## initialize blender
imgRes_x = 720 # recommend > 1080 (UI: Scene > Output > Resolution X)
imgRes_y = 720 # recommend > 1080 
numSamples = 200 # recommend > 200 for paper images
exposure = 1.5 
use_GPU = True
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure, use_GPU)

## read point cloud from numpy
location = (0,0,0.67)
rotation = (0,0,0) 
scale = (.5,.5,.5)
P = np.array([[1,1,1],[-1,1,-1],[-1,-1,1],[1,-1,-1]], dtype=np.float32) # point location
mesh = bt.readNumpyPoints(P,location,rotation,scale)

## (optional) add point colors via scalar (see demo_pointCloudColors.py for setting RGB colors)
PC = np.array([0.,1.,2.,3.]) # point colors
color_map = 'default'
mesh = bt.setPointScalars(mesh, PC, color_map)

## set material ptColor = (RGBA, H, S, V, Bright, Contrast)
ptColor = bt.colorObj([], 0.5, 1.0, 1.0, 0.0, 0.0)
ptSize = 0.3
bt.setMat_pointCloudColored(mesh, ptColor, ptSize)

## set invisible plane (shadow catcher)
bt.invisibleGround(shadowBrightness=0.9)

## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
camLocation = (3, 0, 2)
lookAtLocation = (0,0,0.5)
focalLength = 45 # (UI: click camera > Object Data > Focal Length)
cam = bt.setCamera(camLocation, lookAtLocation, focalLength)

## set light
## Option1: Three Point Light System 
# bt.setLight_threePoints(radius=4, height=10, intensity=1700, softness=6, keyLoc='left')
## Option2: simple sun light
lightAngle = (6, -30, -155) 
strength = 2
shadowSoftness = 0.3
sun = bt.setLight_sun(lightAngle, strength, shadowSoftness)

## set ambient light
bt.setLight_ambient(color=(0.1,0.1,0.1,1)) 

## set gray shadow to completely white with a threshold (optional but recommended)
bt.shadowThreshold(alphaThreshold = 0.05, interpolationMode = 'CARDINAL')

## save blender file so that you can adjust parameters in the UI
bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test.blend')

# ## save rendering
bt.renderImage(outputPath, cam)