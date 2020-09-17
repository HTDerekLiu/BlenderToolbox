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
import math
import numpy as np

def copyArrowToVertex(mesh, tmpArrow, VIdx, VNs = None):
    bpy.ops.object.select_all(action = 'DESELECT')
    tmpArrow.select_set(True)
    bpy.context.view_layer.objects.active = tmpArrow
    for ii in range(len(VIdx)):
        print("copy progress " + str(ii) + "/" + str(len(VIdx)))
        v = VIdx[ii]
        pos = mesh.matrix_world @ mesh.data.vertices[v].co
        bpy.ops.object.duplicate({"object" : tmpArrow}, linked=True)
        objCopy = bpy.context.object
        objCopy.location = pos

        # if not prescribed normals, then draw along vertex normal
        if VNs is None: 
            VN = mesh.matrix_world @ mesh.data.vertices[v].normal
            VN = VN.normalized()
        else:
            VN = VNs[ii,:]
            VN = VN / np.linalg.norm(VN)
        phi = math.atan2(VN[1], VN[0]) 
        theta = math.acos(VN[2]) 
        objCopy.rotation_euler[1] = theta 
        objCopy.rotation_euler[2] = phi 

    
        