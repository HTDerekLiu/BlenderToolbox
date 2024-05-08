# # if you want to call the toolbox the old way with `blender -b -P demo_XXX.py`, then uncomment these two lines
# import sys, os
# sys.path.append("../../BlenderToolbox/")
import blendertoolbox as bt 
import bpy
import os
import numpy as np
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

## read mesh
location = (0.42,-0.1,-0.1) 
rotation = (0,0,50) 
scale = (0.025,0.025,0.025)
mesh = bt.readMesh("../meshes/fat_dragon_39507.obj", location, rotation, scale)
meshColor = bt.colorObj((1,1,1,1), 0.5, 1.0, 1.0, 0.0, 0.0)
bt.setMat_plastic(mesh, meshColor)

## read vector fields 
P = np.loadtxt("../meshes/fat_dragon_source_locations.txt") # Nx3 array of vector source locations
P_vec = np.loadtxt("../meshes/fat_dragon_vectors.txt") # Nx3 array of vector directions

## set arrow material
thickness = 0.2 # this can be found in the geometry node graph
length = 0.5 # this can be found in the geometry node graph
arrow_mesh = bt.createVectorFieldMesh(P, P_vec, thickness, length, location, rotation, scale)
arrow_color = bt.colorObj(bt.derekBlue, 0.5, 1.0, 1.0, 0.0, 2.0)
bt.setMat_plastic(arrow_mesh, arrow_color)

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