import sys
sys.path.append('/Users/hsuehtil/Dropbox/BlenderToolbox/') # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import os, bpy, bmesh
import numpy as np
cwd = os.getcwd()

'''
RENDER AN IMAGE STEP-BY-STEP:
1. copy "template.py" to your preferred local folder
2. In "template.py":
    - change meshPath
    - set your desired material (select one from the demo scripts)
3. run "blender --background --python template.py" in terminal, then terminate the code when it starts rendering. This step outputs a "test.blend"
4. open "test.blend" with your blender software
5. In blender UI, adjust:
    - location, rotation, scale of the mesh
    - material parameters
6. In "template.py":
    - type in the adjusted parameters from UI 
    - set outputPath and increase imgRes_x, imgRes_y, numSamples
7. run "blender --background --python template.py" again to output your final image
'''

outputPath = os.path.join(cwd, './template.png') # make it abs path for windows

## initialize blender
imgRes_x = 720 # recommend > 1080 (UI: Scene > Output > Resolution X)
imgRes_y = 720 # recommend > 1080 
numSamples = 200 # recommend > 200 for paper images
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read mesh (choose either readPLY or readOBJ)
meshPath = './meshes/spot.ply'
location = (1.12, -0.14, 0) # (UI: click mesh > Transform > Location)
rotation = (90, 0, 227) # (UI: click mesh > Transform > Rotation)
scale = (1.5,1.5,1.5) # (UI: click mesh > Transform > Scale)
mesh = bt.readMesh(meshPath, location, rotation, scale)

## set shading (uncomment one of them)
bpy.ops.object.shade_smooth() # Option1: Gouraud shading
# bpy.ops.object.shade_flat() # Option2: Flat shading
# bt.edgeNormals(mesh, angle = 10) # Option3: Edge normal shading

## subdivision
bt.subdivision(mesh, level = 2)

###########################################
## Set your material here (see other demo scripts)

# colorObj(RGBA, H, S, V, Bright, Contrast)
RGBA = (144.0/255, 210.0/255, 236.0/255, 1)
meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
bt.setMat_plastic(mesh, meshColor)

## End material
###########################################

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
bpy.ops.wm.save_mainfile(filepath='./test.blend')

## save rendering
bt.renderImage(outputPath, cam)