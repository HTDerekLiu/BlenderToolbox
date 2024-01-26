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
import numpy as np

def readNumpyMesh(V,F,location,rotation_euler,scale):
    """
    this function creates a blender mesh from numpy array

    Inputs
    V: |V|x3 array of vertex locations
    F: |F|xn array of face indices
    location: (3,) long tuple of mesh locations (same values as UI)
    rotation: (3,) long tuple of rotation angles (same values as UI)
    scale: (3,) long tuple of per-axis mesh scaling (same values as UI)

    Output
    mesh_obj a blender object
    """
    x = rotation_euler[0] * 1.0 / 180.0 * np.pi 
    y = rotation_euler[1] * 1.0 / 180.0 * np.pi 
    z = rotation_euler[2] * 1.0 / 180.0 * np.pi 
    angle = (x,y,z)

    mesh = bpy.data.meshes.new(name='numpy mesh')
    mesh.from_pydata(V,[],F)
    mesh.update()
    mesh.validate()
    mesh_obj = bpy.data.objects.new('numpy mesh object', mesh)
    mesh_obj.location = location
    mesh_obj.rotation_euler = angle
    mesh_obj.scale = scale
    bpy.context.scene.collection.objects.link(mesh_obj)
    bpy.context.view_layer.update()
    return mesh_obj 

    # if vertex_colors is not None: # if specified vertex colors
    #     # Note: blender use name to reference an object, so I use "Col" here. If we change to another name, we will need to change other parts in the toolbox
    #     color_layer = mesh.vertex_colors.new(name='Col') 
    #     idx = 0
    #     if V.shape[0] != vertex_colors.shape[0]:
    #         raise ValueError('Error in "readNumpyMesh": vertex colors must have the same length as the number of vertices')
    #     for vIdx in F.flatten():
    #         # blender use per-corner color so we loop over each face one-by-one
    #         color_layer.data[idx].color = (vertex_colors[vIdx,0],vertex_colors[vIdx,1],vertex_colors[vIdx,2], 1.0)
    #         idx += 1

    # if face_colors is not None:
    #     color_layer = mesh.vertex_colors.new(name='Col') 
    #     idx = 0
    #     if F.shape[0] != face_colors.shape[0]:
    #         raise ValueError('Error in "readNumpyMesh": face colors must have the same length as the number of faces')
    #     for ii in range(F.shape[0]):
    #         color_layer.data[ii*3].color = (face_colors[ii,0],face_colors[ii,1],face_colors[ii,2], 1.0)
    #         color_layer.data[ii*3+1].color = (face_colors[ii,0],face_colors[ii,1],face_colors[ii,2], 1.0)
    #         color_layer.data[ii*3+2].color = (face_colors[ii,0],face_colors[ii,1],face_colors[ii,2], 1.0)