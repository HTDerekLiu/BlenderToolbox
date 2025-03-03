import os, bpy
import numpy as np

from . blenderInit import blenderInit
from . readMesh import readMesh
from . readNumpyPoints import readNumpyPoints
from . setMat_pointCloud import setMat_pointCloud
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

def render_point_cloud_default(args):
  ## initialize blender
  imgRes_x = args["image_resolution"][0]
  imgRes_y = args["image_resolution"][1]
  numSamples = args["number_of_samples"]
  exposure = 1.5 
  use_GPU = True
  blenderInit(imgRes_x, imgRes_y, numSamples, exposure, use_GPU)

  ## read mesh
  location = args["mesh_position"]
  rotation = args["mesh_rotation"]
  scale = args["mesh_scale"]
  if "mesh_path" in args:
    meshPath = args["mesh_path"]
    mesh = readMesh(meshPath, location, rotation, scale)
  elif "mesh_path" not in args and "vertices" in args:
    P = args["vertices"]
    mesh = readNumpyPoints(P,location,rotation,scale)
  else:
    raise ValueError("one should provide either [mesh_path] or [vertices, faces] in the args")   

  ## default render for point cloud
  RGB = args["mesh_RGB"]
  RGBA = (RGB[0], RGB[1], RGB[2], 1)
  ptColor = colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 0.0)
  ptSize = args["point_size"]
  setMat_pointCloud(mesh, ptColor, ptSize)

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
  bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test.blend')

  ## save rendering
  renderImage(os.path.abspath(args["output_path"]), cam)