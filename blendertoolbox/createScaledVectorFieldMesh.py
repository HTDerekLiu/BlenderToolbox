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
import bpy, bmesh
import numpy as np
import math
import mathutils

# TODO: for some reasons, I cannot use python to link face area to scale the arrows
def createScaledVectorFieldMesh(mesh, P, PN, thickness, length, per_vector_scales):

    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1))
    arrow_obj = bpy.data.objects[-1]
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center = 'MEDIAN') # set the object origin to the bottom
    bpy.ops.object.editmode_toggle()
    arrow_bmesh = bmesh.from_edit_mesh(arrow_obj.data)
    vertices= [v for v in arrow_bmesh.verts]
    for v in vertices:
        if v.index == 81: # 81 is the vertex index for the top UV sphere
            bpy.ops.mesh.select_all(action = 'DESELECT')
            v.select = True
            bpy.ops.transform.translate(value = (0,0,1),constraint_axis = (False, False, True),orient_type = 'GLOBAL',use_proportional_edit=True, proportional_edit_falloff='LINEAR')
    bpy.ops.object.editmode_toggle()
    arrow_obj.location = (1e5,1e5,1e5) # move it out of the scene
    bpy.ops.object.shade_smooth()

    mat = bpy.data.materials.new('MeshMaterial')
    arrow_obj.data.materials.append(mat)
    arrow_obj.active_material = mat
    mat.diffuse_color = (1,1,1,1)

    for ii in range(P.shape[0]): 
        p1_ref = mathutils.Vector((P[ii,0], P[ii,1], P[ii,2]))
        p2_ref = mathutils.Vector((P[ii,0]+PN[ii,0], P[ii,1]+PN[ii,1], P[ii,2]+PN[ii,2]))

        p1 = mesh.matrix_world @ p1_ref
        p2 = mesh.matrix_world @ p2_ref
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dz = p2[2] - p1[2]
        dist = math.sqrt(dx**2 + dy**2 + dz**2) 

        # cylinder.duplicate
        # bpy.context.selected_objects.clear()
        # cylinder.select_set(True)
        bpy.ops.object.duplicate( linked=True)  # annoying I can't specify object i want to apply this to in here

        # bpy.context.selected_objects.clear()
        objCopy = bpy.context.active_object

        objCopy.dimensions = (thickness, thickness, dist * per_vector_scales[ii] * length)
        objCopy.location = (dx/2 + p1[0], dy/2 + p1[1], dz/2 + p1[2])
        phi = math.atan2(dy, dx) 
        theta = math.acos(dz/dist) 
        bpy.context.object.rotation_euler[1] = theta 
        bpy.context.object.rotation_euler[2] = phi 

    return arrow_obj
