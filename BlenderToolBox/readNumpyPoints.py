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

def readNumpyPoints(P,location,rotation_euler,scale,point_colors=None):
    """
    this function creates a blender mesh from numpy array

    Inputs
    P: |V|x3 array of vertex locations
    location: (3,) long tuple of mesh locations (same values as UI)
    rotation: (3,) long tuple of rotation angles (same values as UI)
    scale: (3,) long tuple of per-axis mesh scaling (same values as UI)
    point_colors: (optional) |V|x3 list of point colors, each row is a rgb color between [0,1]

    Output
    mesh_obj a blender object
    """
    x = rotation_euler[0] * 1.0 / 180.0 * np.pi 
    y = rotation_euler[1] * 1.0 / 180.0 * np.pi 
    z = rotation_euler[2] * 1.0 / 180.0 * np.pi 
    angle = (x,y,z)

    mesh = bpy.data.meshes.new(name='numpy point cloud')
    F = [np.arange(P.shape[0])] # the face of a point cloud is a single large polygonal face because blender mesh only support face colors
    mesh.from_pydata(P,[],F)
    mesh.update()
    mesh.validate()
    mesh_obj = bpy.data.objects.new('numpy point cloud object', mesh)
    mesh_obj.location = location
    mesh_obj.rotation_euler = angle
    mesh_obj.scale = scale
    bpy.context.scene.collection.objects.link(mesh_obj)
    bpy.context.view_layer.update()

    if point_colors is not None: # if specified vertex colors
        # Note: blender use name to reference an object, so I use "Col" here. If we change to another name, we will need to change other parts in the toolbox
        color_layer = mesh.vertex_colors.new(name='Col') 
        if P.shape[0] != point_colors.shape[0]:
            raise ValueError('Error in "readNumpyPoints": point colors must have the same length as the number of points')
        for vIdx in range(P.shape[0]):
            # blender use per-corner color so we loop over each face one-by-one
            color_layer.data[vIdx].color = (point_colors[vIdx,0],point_colors[vIdx,1],point_colors[vIdx,2], 1.0)
    return mesh_obj 