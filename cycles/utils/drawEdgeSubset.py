import bpy
import math
import numpy as np

def drawEdgeSubset(mesh, E, r, colorList = None):
    for ii in range(E.shape[0]): 
        p1Idx = E[ii,0]
        p2Idx = E[ii,1]
        p1 = mesh.matrix_world @ mesh.data.vertices[p1Idx].co
        p2 = mesh.matrix_world @ mesh.data.vertices[p2Idx].co
        x1 = p1[0]
        y1 = p1[1]
        z1 = p1[2]
        x2 = p2[0]
        y2 = p2[1]
        z2 = p2[2]
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1    
        dist = math.sqrt(dx**2 + dy**2 + dz**2)
        bpy.ops.mesh.primitive_cylinder_add(
            radius = r, 
            depth = dist,
            location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
        ) 
        phi = math.atan2(dy, dx) 
        theta = math.acos(dz/dist) 
        bpy.context.object.rotation_euler[1] = theta 
        bpy.context.object.rotation_euler[2] = phi 

        if colorList is not None:
            mat = bpy.data.materials.new('MeshMaterial')
            bpy.context.object.data.materials.append(mat)
            bpy.context.object.active_material = mat
            if len(colorList) != 4:
                mat.diffuse_color = colorList[ii,:]
            else:
                mat.diffuse_color = colorList