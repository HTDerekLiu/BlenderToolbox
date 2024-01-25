import sys, os
sys.path.append(os.path.join(os.path.abspath(os.getcwd()),'..')) # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import bpy, bmesh
import numpy as np
cwd = os.getcwd()

outputPath = os.path.join(cwd, './demo_slicePlane.png') 

## initialize blender
imgRes_x = 480 
imgRes_y = 480 
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read mesh (decoration for the scene)
location = (1.12, -0.14, 0) 
rotation = (90, 0, 227)
scale = (1.5,1.5,1.5) 
meshPath = '../meshes/spot.obj'
mesh = bt.readMesh(meshPath, location, rotation, scale)
bpy.ops.object.shade_smooth() 
bt.subdivision(mesh, level = 2)
meshColor = bt.colorObj(bt.derekBlue, 0.5, 1.0, 1.0, 0.0, 2.0)
bt.setMat_plastic(mesh, meshColor)

## read slice plane
meshPath = '../meshes/slice_plane.obj'
mesh = bt.readMesh(meshPath, location, rotation, scale)
bpy.ops.object.shade_flat() 
bt.subdivision(mesh, level = 0)

scalar = np.load("../meshes/slice_plane_scalar.npy")
mesh = bt.vertexScalarToUV(mesh, scalar)

useless = (0,0,0,1)
meshColor = bt.colorObj(useless, 0.5, 1.3, 1.0, 0.0, 0.4)
texturePath = '../meshes/RdBu_black.png' 
alpha = 0.75 # the smaller the more transparent
bt.setMat_texture(mesh, texturePath, meshColor, alpha)

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