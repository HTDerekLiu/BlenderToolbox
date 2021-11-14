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

def createArrow(length, location, rotation_euler, scale):
    # create arrow 
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, location=(0, 0, 0))
    sphere = bpy.data.objects['Sphere']
    
    bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2, enter_editmode=False, location=(0, 0, 0))
    cone = bpy.data.objects['Cone']
    cone.location[2] = length
    cone.scale[2] = length

    # select cone
    bpy.ops.object.select_all(action = 'DESELECT')
    sphere.select_set(True)
    bpy.context.view_layer.objects.active = sphere

    bpy.ops.object.modifier_add(type='BOOLEAN')
    sphere.modifiers["Boolean"].operation = 'UNION'
    sphere.modifiers["Boolean"].object = cone
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

    bpy.ops.object.select_all(action = 'DESELECT')
    cone.select_set(True)
    bpy.context.view_layer.objects.active = cone
    bpy.ops.object.delete()  

    # move 
    x = rotation_euler[0] * 1.0 / 180.0 * np.pi 
    y = rotation_euler[1] * 1.0 / 180.0 * np.pi 
    z = rotation_euler[2] * 1.0 / 180.0 * np.pi 
    angle = (x,y,z)
    sphere.location = location
    sphere.rotation_euler = angle
    sphere.scale = scale

    return sphere