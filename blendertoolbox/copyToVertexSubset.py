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

def copyToVertexSubset(mesh, templateObj, VIdx):
    bpy.ops.object.select_all(action = 'DESELECT')
    templateObj.select_set(True)
    bpy.context.view_layer.objects.active = templateObj
    for ii in VIdx:
        Vloc = mesh.matrix_world @ mesh.data.vertices[int(ii)].co

        bpy.ops.object.duplicate( linked=True)  # annoying I can't specify object i want to apply this to in here
        bpy.context.selected_objects.clear()
        templateObj.select_set(True)

        objCopy = bpy.context.active_object

        objCopy.location = Vloc