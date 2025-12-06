# Copyright 2025 Hsueh-Ti Derek Liu
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

def setGraphMesh(V, E, location, rotation, scale):
    # =============================================================================
    # Create graph mesh from V and E
    # =============================================================================
    mesh_data = bpy.data.meshes.new("GraphMesh")
    mesh_data.from_pydata(V, E, [])  # Empty list for faces as it's a graph

    obj = bpy.data.objects.new("GraphObject", mesh_data)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    obj.location = location
    x = rotation[0] * 1.0 / 180.0 * np.pi 
    y = rotation[1] * 1.0 / 180.0 * np.pi 
    z = rotation[2] * 1.0 / 180.0 * np.pi 
    angle = (x,y,z)
    obj.rotation_euler = angle
    obj.scale = scale
    return obj