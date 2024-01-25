import sys, os
sys.path.append(os.path.join(os.path.abspath(os.getcwd()),'..')) # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import bpy, bmesh
import numpy as np
cwd = os.getcwd()

outputPath = os.path.join(cwd, './demo_blend_background.png') # make it abs path for windows

## initialize blender
imgRes_x = 600 
imgRes_y = 480 
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read mesh (choose either readPLY or readOBJ)
meshPath = '../meshes/spot.ply'
location = (1.12, -0.14, 1.36) # (UI: click mesh > Transform > Location)
rotation = (90, 0, 227) # (UI: click mesh > Transform > Rotation)
scale = (1.5,1.5,1.5) # (UI: click mesh > Transform > Scale)
mesh = bt.readMesh(meshPath, location, rotation, scale)

## set shading (uncomment one of them)
bpy.ops.object.shade_smooth() 

## subdivision
bt.subdivision(mesh, level = 2)

# # set material
meshColor = bt.colorObj(bt.derekBlue, 0.5, 1.0, 1.0, 0.0, 2.0)
bt.setMat_plastic(mesh, meshColor)

# ## set invisible plane (shadow catcher)
# bt.invisibleGround(shadowBrightness=0.9)

# import background from another scene
background_RGBA = (0.043, 0.137, 0.233, 1)
is_background_transparent = False
bt.set_background(background_RGBA, is_background_transparent)

file_path = "path/to/*.blend"
bt.import_scene_from_blend(file_path)

## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
camLocation = (31.403, 0.16536, 5.4295)
rotation = (91.2,0,90)
focalLength = 90 # (UI: click camera > Object Data > Focal Length)
cam = bt.setCamera_from_UI(camLocation, rotation, focalLength)

## save blender file so that you can adjust parameters in the UI
bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test.blend')

## save rendering
bt.renderImage(outputPath, cam)