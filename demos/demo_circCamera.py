import sys
sys.path.append('/Users/hsuehtil/Dropbox/BlenderToolbox/') # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import os, bpy, bmesh
import numpy as np
cwd = os.getcwd()

outputHeader = os.path.join(cwd, './demo_circCamera_') # make it abs path for windows

## initialize blender
imgRes_x = 480 
imgRes_y = 480 
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read mesh (choose either readPLY or readOBJ)
meshPath = '../meshes/spot.ply'
location = (1.12, -0.14, 0) # (UI: click mesh > Transform > Location)
rotation = (90, 0, 227) # (UI: click mesh > Transform > Rotation)
scale = (1.5,1.5,1.5) # (UI: click mesh > Transform > Scale)
mesh = bt.readMesh(meshPath, location, rotation, scale)

## set shading (uncomment one of them)
bpy.ops.object.shade_smooth() 

## subdivision
bt.subdivision(mesh, level = 2)

# # set material
# colorObj(RGBA, H, S, V, Bright, Contrast)
RGBA = (144.0/255, 210.0/255, 236.0/255, 1)
meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
bt.setMat_plastic(mesh, meshColor)

## set invisible plane (shadow catcher)
bt.invisibleGround(shadowBrightness=0.9)

## set camera 
R = 3 # radius of the circle camera path
H = 2 # height of the circle camera path
lookAtPos = (0,0,0.5) # look at position
startAngle = 0 # camera starting angle from positive x-axis
focalLength = 45
duration = 5 # number of frames in total for 360 degrees
cam = bt.setCameraPath(R, H, lookAtPos, focalLength,duration,startAngle)

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
bt.renderAnimation(outputHeader, cam, duration)