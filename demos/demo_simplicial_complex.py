# # if you want to call the toolbox the old way with `blender -b -P demo_XXX.py`, then uncomment these two lines
import sys, os
sys.path.append("../../BlenderToolbox/")
import blendertoolbox as bt 
import bpy
import os
import numpy as np

outputPath = os.path.abspath('./demo_simplicial_complex.png') # make it abs path for windows

## initialize blender
imgRes_x = 480 
imgRes_y = 480 
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read mesh from numpy array
location = (0,0,0.67) 
rotation = (0,0,0) 
scale = (.5,.5,.5)
V = np.array([
    [1,1,1],
    [-1,1,-1],
    [-1,-1,1],
    [1,-1,-1],
    [2,1,0],
    ], dtype=np.float32) # vertex list
F = np.array([
    [0,1,2],
    [0,2,3],
    [0,3,1],
    [2,1,3]
    ], dtype=np.int32) # face list
E = np.array([
    [0,1],
    [0,2],
    [0,3],
    [1,2],
    [1,3],
    [2,3],
    [0,4],
    ], dtype=np.int32) # edge list
meshFace, meshCurveNetwork = bt.readSimplicialComplex(V,E,F,location,rotation,scale)

nodeSize = 0.15
edgeThickness = 0.1
nodeColor = bt.colorObj(bt.coralRed, H=0.5, S=1.0, V=1.0, B=0.0, C=0.0)
edgeColor = bt.colorObj(bt.iglGreen, H=0.5, S=1.0, V=1.0, B=0.0, C=0.0)
faceColor = bt.colorObj(bt.derekBlue, H=0.5, S=1.0, V=1.0, B=0.0, C=0.0)
bt.setMat_simplicialComplex(meshFace, meshCurveNetwork, nodeSize, edgeThickness, nodeColor, edgeColor, faceColor)

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