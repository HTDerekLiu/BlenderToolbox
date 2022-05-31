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

def setPointColors(mesh_obj, C):
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

    # assigning vertex colors
    color_layer = mesh.vertex_colors.new(name='Col') 
    idx = 0
    for fIdx in range(nF):
        for vIdx in mesh.polygons[fIdx].vertices:
            color_layer.data[idx].color = (C[vIdx,0],C[vIdx,1],C[vIdx,2], 1.0)
            idx += 1
    
    return mesh_obj



