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
import bpy
import bmesh
import numpy as np
from . initColorNode import initColorNode

def genPolylineMesh(mesh, v_list, r, bdColor):
    nV = len(mesh.data.vertices)
    V = np.zeros((nV, 3), dtype = float)
    for ii in range(nV):
        V[ii,:] = mesh.matrix_local.to_3x3() @ mesh.data.vertices[int(ii)].co
        V[ii,0] += mesh.matrix_local[0][3]
        V[ii,1] += mesh.matrix_local[1][3]
        V[ii,2] += mesh.matrix_local[2][3]

    # create a mesh
    bdMesh = bpy.data.meshes.new('boundary') 
    bdObj = bpy.data.objects.new('objBoundary', bdMesh) 
    bpy.context.scene.collection.objects.link(bdObj)
    bm = bmesh.new()  
    bm.from_mesh(bdMesh) 

    # add vertices
    VList =  []
    for ii in range(len(v_list)):
        v = bm.verts.new( V[v_list[ii],:] )
        VList.append(v)
    
    # addedges
    for ii in range(len(v_list)-1):
        v1 = VList[ii]
        v2 = VList[ii+1]
        bm.edges.new((v1, v2))


    # update bmesh
    bm.to_mesh(bdMesh)
    bm.free()

    # bevel with a circle
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bdObj
    bdObj.select_set(state=True)
    bpy.ops.object.convert(target='CURVE')
    bpy.ops.curve.primitive_bezier_circle_add(radius=r, location=(1e5, 1e5, 1e5))
    circ = bpy.context.object
    bdObj.data.bevel_object = circ
    bpy.ops.object.shade_smooth()

    # # subdivision
    level = 2
    bpy.context.view_layer.objects.active = bdObj
    bpy.ops.object.modifier_add(type='SUBSURF')
    bdObj.modifiers["Subdivision"].render_levels = level
    bdObj.modifiers["Subdivision"].levels = level 
    bdObj.data.bevel_depth = r

    # add material
    mat = bpy.data.materials.new('MeshMaterial')
    bdObj.data.materials.append(mat)
    bdObj.active_material = mat
    mat.use_nodes = True
    tree = mat.node_tree

    # init color node
    BCNode = initColorNode(tree, bdColor)

    # set principled BSDF
    tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.7
    tree.nodes["Principled BSDF"].inputs['Sheen Tint'].default_value = 0
    tree.links.new(BCNode.outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])
