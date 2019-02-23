import bpy
from utils.colorMap import *

def setVColor(mesh, C, colormap = 'default'):
    C_rgb = colorMap(C, colormap)
    mesh.data.vertex_colors.new()
    color_layer = mesh.data.vertex_colors[-1]
    ii = 0
    for face in mesh.data.polygons:
        for VIdx in face.vertices:
            color_layer.data[ii].color = C_rgb[VIdx,:]
            ii += 1

    