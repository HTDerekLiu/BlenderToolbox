import sys, os
sys.path.append(os.path.join(os.path.abspath(os.getcwd()),'..')) # change this to your path to “path/to/BlenderToolbox/
import blendertoolbox as bt
import bpy, bmesh
import numpy as np
cwd = os.getcwd()


outputPath = os.path.join(cwd, './demo_drawLines.png') # make it abs path for windows

## initialize blender
imgRes_x = 480 
imgRes_y = 480 
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

# create original local frame
orig = np.array([0.,-0.4,0.1])
lineVec = np.array([[1,0,0],[0,1,0],[0,0,1]])

p1List = np.tile(orig[None,:], (lineVec.shape[0],1))
p2List = p1List + lineVec
colorList = np.array([[1,0,0,1],[0,1,0,1],[0,0,1,1]])
radius = 0.1
bt.drawLines(p1List, p2List, radius, colorList)

## set invisible plane (shadow catcher)
bt.invisibleGround(shadowBrightness=0.9)

## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
camLocation = (3, 0, 2)
lookAtLocation = (0,0,0.5)
focalLength = 45 # (UI: click camera > Object Data > Focal Length)
cam = bt.setCamera(camLocation, lookAtLocation, focalLength)

## set light
lightAngle = (6, -30, -155) 
strength = 2
shadowSoftness = 0.3
sun = bt.setLight_sun(lightAngle, strength, shadowSoftness)

## set ambient light
bt.setLight_ambient(color=(0.1,0.1,0.1,1)) 

## set gray shadow to completely white with a threshold 
bt.shadowThreshold(alphaThreshold = 0.05, interpolationMode = 'CARDINAL')

## save blender file so that you can adjust parameters in the UI
bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test.blend')

## save rendering
bt.renderImage(outputPath, cam)