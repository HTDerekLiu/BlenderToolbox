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

def setPointScalars(mesh_obj, C, color_map_name = 'default'):
    """
    This function set per vertex/face colors of a mesh with a numpy array of RGB colors (between 0 and 1)

    Inputs
    mesh_obj: bpy.object of the mesh
    C: |V| numpy array of point scalars
    color_map_name: name of the color maps (see colorMap.py)

    Outputs
    mesh_obj
    """
    """
    This function set per vertex/face colors of a mesh with a numpy array of RGB colors (between 0 and 1)

    Inputs
    mesh_obj: bpy.object of the point cloud
    C: |V|x3 numpy array of point colors, each row is a rgb color between [0,1]

    Outputs
    mesh_obj
    """
    mesh = mesh_obj.data
    nV = len(mesh.vertices)
    nF = len(mesh.polygons)

    # guess the type of colors
    if C.shape[0] != nV:
        raise ValueError('Error in "setPointColors": input color format must be eithe |P|x3 array of point colors')

    if nF != 1:
        raise ValueError('Error in "setPointColors": please switch to "readNumpyPoints" to read the input point cloud')
    
    C_RGB = colorMap(C, color_map_name)

    # assigning vertex colors
    color_layer = mesh.vertex_colors.new(name='Col') 
    idx = 0
    for fIdx in range(nF):
        for vIdx in mesh.polygons[fIdx].vertices:
            color_layer.data[idx].color = (C_RGB[vIdx,0],C_RGB[vIdx,1],C_RGB[vIdx,2], 1.0)
            idx += 1
    
    return mesh_obj



