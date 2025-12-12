# # if you want to call the toolbox the old way with `blender -b -P demo_XXX.py`, then uncomment these two lines
# import sys, os
# sys.path.append("../../BlenderToolbox/")

import blendertoolbox as bt 
import bpy
import os
import numpy as np




if __name__ == "__main__":

    outputPath = os.path.abspath('./demo_graph.png')

    ## initialize blender
    imgRes_x = 480 
    imgRes_y = 480 
    numSamples = 100 
    exposure = 1.5 
    bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

    location = (0.26, 0, 0.6) # (UI: click mesh > Transform > Location)
    rotation = (90, 0, 227) # (UI: click mesh > Transform > Rotation)
    scale = (0.8, 0.8, 0.8) # (UI: click mesh > Transform > Scale)
    V = np.load('../meshes/spot_V.npy').astype(np.float32)
    E = np.load('../meshes/spot_E.npy').astype(np.int32)
    mesh = bt.setGraphMesh(V, E, location, rotation, scale)

    edge_thickness = 0.005        # Thickness of graph edges
    node_size = 0.015             # Size of graph nodes (vertices)
    edge_resolution = 8          # Smoothness of edge cylinders (higher = smoother)
    edge_color = bt.colorObj(bt.derekBlue, H=0.5, S=1.0, V=1.0, B=0.0, C=0.0)
    node_color = bt.colorObj(bt.coralRed, H=0.5, S=1.0, V=1.0, B=0.0, C=0.0)
    bt.setMat_graph(mesh, node_size,  edge_thickness, node_color, edge_color, edge_resolution)

    ## set invisible plane (shadow catcher)
    bt.invisibleGround(shadowBrightness=0.9)

    ## set camera
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