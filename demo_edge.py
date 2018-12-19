import sys
sys.path.append('/Users/Hsueh-Ti/Dropbox/BlenderToolbox')

from include import *
import bpy

# # init blender
imgRes_x = 1000
imgRes_y = 1000 
numSamples = 250 # should set it to perhaps 2000 for high quality paper images
blenderInit(imgRes_x, imgRes_y, numSamples)

# # read mesh 
meshPath = './test.ply'
location = (-0.3, 0.6, -0.04)
rotation = (90, 0,0)
scale = (1.5,1.5,1.5)
mesh = readPLY(meshPath, location, rotation, scale)

# # set shading
# bpy.ops.object.shade_smooth()
bpy.ops.object.shade_flat()

# # subdivision
# level = 2
# subdivision(mesh, level)

# # set material (option1: render mesh with edges)
edgeThickness = 0.002
edgeColor = (0,0,0,0)
meshColor = (0.5,0.5,0.5,0)
setMat_edge(mesh, edgeThickness, edgeColor, meshColor)

# # set invisible plane
groundCenter = (0,0,0)
groundSize = 5
invisibleGround(groundCenter, groundSize)

# # ambient occlusion
AOStrength = 1.5
ambientOcclusion(AOStrength)

# # set camera
camLocation = (1.9,2,2.2)
lookAtLocation = (0,0,0.5)
focalLength = 45
cam = setCamera(camLocation, lookAtLocation, focalLength)

# # set sunlight
lightAngle = (-15,-34,-155) 
strength = 4
shadowSoftness = 0.05
sun = setLight_sun(lightAngle, strength, shadowSoftness)

# # set ambient light
ambientColor = (0.1,0.1,0.1)
setLight_ambient(ambientColor)

# # save blender file
bpy.ops.wm.save_mainfile(filepath='./test.blend')

# # save rendering
bpy.data.scenes['Scene'].render.filepath = './test.png'
bpy.data.scenes['Scene'].camera = cam
bpy.ops.render.render(write_still = True)