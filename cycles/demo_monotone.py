# Copyright 2020 Hsueh-Ti Derek Liu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os 
cwd = os.getcwd()
import sys
sys.path.append(cwd)
from include import *
import bpy

outputPath = './results/demo_monotone.png'

# # init blender
imgRes_x = 720  # increase this for paper figures
imgRes_y = 720  # increase this for paper figures
numSamples = 50 # usually increase it to >200 for paper figures
exposure = 1.0
blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

# # read mesh 
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

# # set material Note: discreteColor(bright, pos1, pos2)
numColor = 3
CList = [None] * numColor
CList[0] = discreteColor(brightness=0.8, pos1=None, pos2=None)
CList[1] = discreteColor(brightness=0.3, pos1=0.045, pos2=0.05)
CList[2] = discreteColor(brightness=0.0, pos1=0.2, pos2=0.4)
meshColor = colorObj(derekBlue, 0.5, 1.2, 1.0, 0.0, 0.5) 
silhouetteColor = colorObj(derekBlue, 0.5, 1.2, 1.0 * 0.3, 0.0, 0.5) 
shadowSize = 0.4
setMat_monotone(mesh, meshColor, CList, silhouetteColor, shadowSize)

# # set invisible plane (shadow catcher)
groundCenter = (0,0,0)
shadowLight = 0.95
groundSize = 20
invisibleGround(groundCenter, groundSize, shadowLight)

# # set camera
camLocation = (1.9,2,2.2)
lookAtLocation = (0,0,0.5)
focalLength = 45
cam = setCamera(camLocation, lookAtLocation, focalLength)

# # set sunlight
lightAngle = (-15,-34,-155) 
strength = 2
shadowSoftness = 0.0
sun = setLight_sun(lightAngle, strength, shadowSoftness)

# # set ambient light
ambientColor = (0.2,0.2,0.2,1)
setLight_ambient(ambientColor)

# # composite 
alphaThreshold = 0.05
mode = 'CARDINAL'
shadowThreshold(alphaThreshold,mode)

# # save blender file
bpy.ops.wm.save_mainfile(filepath='./test.blend')

# # # save rendering
renderImage(outputPath, cam)