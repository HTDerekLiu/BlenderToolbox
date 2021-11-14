import os, bpy, bmesh
import numpy as np

from . blenderInit import blenderInit
from . readMesh import readMesh
from . subdivision import subdivision
from . setMat_plastic import setMat_plastic
from . invisibleGround import invisibleGround
from . setCamera import setCamera
from . setLight_sun import setLight_sun
from . setLight_ambient import setLight_ambient
from . shadowThreshold import shadowThreshold
from . renderImage import renderImage

class colorObj(object):
    def __init__(self, RGBA, \
    H = 0.5, S = 1.0, V = 1.0,\
    B = 0.0, C = 0.0):
        self.H = H # hue
        self.S = S # saturation
        self.V = V # value
        self.RGBA = RGBA
        self.B = B # birghtness
        self.C = C # contrast

def render_mesh_default(args):
  ## initialize blender
  imgRes_x = args["image_resolution"][0]
  imgRes_y = args["image_resolution"][1]
  numSamples = args["number_of_samples"]
  exposure = 1.5 
  blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

  ## read mesh (choose either readPLY or readOBJ)
  meshPath = args["mesh_path"]
  location = args["mesh_location"]
  rotation = args["mesh_rotation"]
  scale = args["mesh_scale"]
  mesh = readMesh(meshPath, location, rotation, scale)

  ## set shading (uncomment one of them)
  if args["shading"] == "smooth":
    bpy.ops.object.shade_smooth() 
  elif args["shading"] == "flat":
    bpy.ops.object.shade_flat() 
  else:
    raise ValueError("shading should be either flat or smooth in lazy pipeline")

  ## subdivision
  subdivision(mesh, level = args["subdivision_iteration"])

  ## default render as plastic
  RGB = args["mesh_RGB"]
  RGBA = (RGB[0], RGB[1], RGB[2], 1)
  meshColor = colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
  setMat_plastic(mesh, meshColor)

  ## set invisible plane (shadow catcher)
  invisibleGround(shadowBrightness=0.9)

  ## set camera 
  camLocation = (3, 0, 2)
  lookAtLocation = (0,0,0.5)
  focalLength = 45 # (UI: click camera > Object Data > Focal Length)
  cam = setCamera(camLocation, lookAtLocation, focalLength)

  ## set light
  lightAngle = args["light_angle"]
  strength = 2
  shadowSoftness = 0.3
  sun = setLight_sun(lightAngle, strength, shadowSoftness)

  ## set ambient light
  setLight_ambient(color=(0.1,0.1,0.1,1)) 

  ## set gray shadow to completely white with a threshold (optional but recommended)
  shadowThreshold(alphaThreshold = 0.05, interpolationMode = 'CARDINAL')

  ## save blender file so that you can adjust parameters in the UI
  bpy.ops.wm.save_mainfile(filepath='./test.blend')

  ## save rendering
  renderImage(args["output_path"], cam)