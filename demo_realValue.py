import sys
sys.path.append('/Users/Hsueh-Ti/Dropbox/BlenderToolbox')

from include import *


outputPath = './results/demo_realValue.png'

# # init blender
imgRes_x = 1000 # should set to > 2000 for paper figures
imgRes_y = 1000 # should set to > 2000 for paper figures
numSamples = 100 # should set to >1000 for high quality paper images
exposure = 1.8
blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

# # read mesh 
meshPath = './meshes/spot_10K.ply'
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

# # set color
colormap = 'default'
C = np.loadtxt('./meshes/spot_10K_realVal.txt')
setVColor(mesh,C, colormap)

# # set material
setMat_VColor(mesh)

# # set invisible plane
groundCenter = (0,0,0)
groundSize = 5
shadowDarkeness = 0.18
invisibleGround(groundCenter, groundSize, shadowDarkeness)

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
strength = 2
shadowSoftness = 0.1
sun = setLight_sun(lightAngle, strength, shadowSoftness)

# # set ambient light
ambientColor = (0.1,0.1,0.1)
setLight_ambient(ambientColor)

# # save blender file
bpy.ops.wm.save_mainfile(filepath='./test.blend')

# # save rendering
# bpy.data.scenes['Scene'].render.filepath = outputPath
# bpy.data.scenes['Scene'].camera = cam
# bpy.ops.render.render(write_still = True)