import sys, os
sys.path.append(os.path.join(os.path.abspath(os.getcwd()),'..')) # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import bpy, bmesh
import numpy as np
import math
cwd = os.getcwd()
###
# After blender 3.4 this function requires some changes to update the API of Transfer Attribute nodes. Will do it later.
###
outputPath = os.path.join(cwd, './demo_vectorField.png') # make it abs path for windows

## initialize blender
imgRes_x = 480 
imgRes_y = 480 
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read vector field mesh from numpy array
location = (0.55, 0.07, 0.82) 
rotation = (0,0,56.4) 
scale = (2,2,2)
thickness = 0.03 # this can be found in the geometry node graph
length = 0.1 # this can be found in the geometry node graph
P = np.array([[.1,0,0],[0,.1,0],[0,0,0.1],[-.1,0,0.],[0,-.1,0],[0,0,-.1]], dtype=np.float32)
PN = np.array([[0.5,0,0],[0,1.5,0],[0,0,1],[-.5,0,0],[0,-1.5,0],[0,0,-1]], dtype=np.float32) 

mesh = bt.createVectorFieldMesh(P, PN, thickness, length, location, rotation, scale)

# set plastic material
meshColor = bt.colorObj(bt.derekBlue, 0.5, 1.0, 1.0, 0.0, 2.0)
bt.setMat_plastic(mesh, meshColor)

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