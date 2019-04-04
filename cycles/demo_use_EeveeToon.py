import sys
sys.path.append('/Users/hsuehtil/Dropbox/BlenderToolbox/cycles')
from include import *
import bpy

outputPath = './results/demo_EeveeToon.png'

# # init blender
imgRes_x = 720 # should set to > 2000 for paper figures
imgRes_y = 720 # should set to > 2000 for paper figures
numSamples = 50 # should set to >1000 for high quality paper images
exposure = 1.0 # need to double check
blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

# read mesh 
meshPath = '../meshes/spot.ply'
location = (-0.3, 0.6, -0.04)
rotation = (90, 0,0)
scale = (1.5,1.5,1.5)
mesh = readPLY(meshPath, location, rotation, scale)

# # set shading
bpy.ops.object.shade_smooth()
# bpy.ops.object.shade_flat()

# # subdivision
level = 2
subdivision(mesh, level)

# append shader
mat = loadShader('EeveeToon', mesh)

# EEVEETOON parameters
mat.inputs[0].default_value = 10.0 # ShadowBanding
mat.inputs[1].default_value = 0.7 # Grow
mat.inputs[2].default_value = 0.32 # ShadowSoftness
mat.inputs[3].default_value = derekBlue # MonoColor
mat.inputs[4].default_value = 1.0 # MonoSat
mat.inputs[5].default_value = 0.1 # MonoDuoMix
mat.inputs[6].default_value = (0.7,0.7,0.7,1) # ColShadow
mat.inputs[7].default_value = derekBlue # ColHightlight

# # set invisible plane (shadow catcher)
# groundCenter = (0,0,0)
# shadowDarkeness = 0.7
# groundSize = 20
# invisibleGround(groundCenter, groundSize, shadowDarkeness)

# # set camera
camLocation = (1.9,2,2.2)
lookAtLocation = (0,0,0.5)
focalLength = 45
cam = setCamera(camLocation, lookAtLocation, focalLength)

# # set sunlight
lightAngle = (-15,-34,-155) 
strength = 2
shadowSoftness = 0.1
sun = setLight_sun(lightAngle, strength, shadowSoftness)

# # set ambient light
# ambientColor = (0.9,0.9,0.9,1)
# setLight_ambient(ambientColor)

# # save blender file
bpy.ops.wm.save_mainfile(filepath='./test.blend')

# # save rendering
bpy.data.scenes['Scene'].render.filepath = outputPath
bpy.data.scenes['Scene'].camera = cam
bpy.ops.render.render(write_still = True)
