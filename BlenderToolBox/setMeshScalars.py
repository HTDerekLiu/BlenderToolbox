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
from . colorMap import colorMap

def setMeshScalars(mesh_obj, C, color_map_name = 'default', type = None):
    """
    This function set per vertex/face colors of a mesh with a numpy array of RGB colors (between 0 and 1)

    Inputs
    mesh_obj: bpy.object of the mesh
    C: |V| (|F|) numpy array of vertex (face) scalars, each row is a rgb color between [0,1]
    color_map_name: name of the color maps (see colorMap.py)
    type: a string of either "vertex" or "face" specifying the type of colors. One can also use None to let the program figure it out

    Outputs
    mesh_obj
    """
    mesh = mesh_obj.data
    nV = len(mesh.vertices)
    nF = len(mesh.polygons)
    nC = len(C.flatten())

    # guess the type of colors
    if type is None:
        if nC == nV:
            print('you did not specify scalar type in "setMeshScalars", it guesses the scalar data is vertex scalars')
            type = 'vertex' 
        elif nC == nF:
            print('you did not specify scalar type in "setMeshScalars", it guesses the scalar data is face scalars')
            type = 'face' 
        else:
            raise ValueError('Error in "setMeshScalars": input scalar format must be eithe (|V|,) array of vertex scalars or (|F|,) array of face scalars')

    # check input array size
    if type is 'vertex': # if vertex colors
        if C.shape[0] != nV:
            raise ValueError('Error in "setMeshScalars": vertex scalar must have the same length as the number of vertices')
    elif type is 'face': # if face colors
        if C.shape[0] != nF:
            raise ValueError('Error in "setMeshScalars": face scalar must have the same length as the number of faces')
    else:
        raise ValueError('type needs to be either "vertex" or "face" or None')

    # turn scalar into colors
    C_RGB = colorMap(C, color_map_name)

    # assigning vertex colors
    if type is 'vertex':
        color_layer = mesh.vertex_colors.new(name='Col') 
        nF = len(mesh.polygons)
        idx = 0
        for fIdx in range(nF):
            for vIdx in mesh.polygons[fIdx].vertices:
                color_layer.data[idx].color = (C_RGB[vIdx,0],C_RGB[vIdx,1],C_RGB[vIdx,2], 1.0)
                idx += 1
    elif type is 'face':
        color_layer = mesh.vertex_colors.new(name='Col') 
        idx = 0
        for fIdx in range(nF):
            for vIdx in mesh.polygons[fIdx].vertices:
                color_layer.data[idx].color = (C_RGB[fIdx,0],C_RGB[fIdx,1],C_RGB[fIdx,2], 1.0)
                idx += 1
    
    return mesh_obj



