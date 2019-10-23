import bpy
from include import *

def copyToVertexSubset(mesh, templateObj, VIdx):
    for ii in VIdx:
        Vloc = mesh.matrix_world @ mesh.data.vertices[int(ii)].co
        bpy.ops.object.duplicate({"object" : templateObj}, linked=True)
        objCopy = bpy.context.object
        objCopy.location = Vloc