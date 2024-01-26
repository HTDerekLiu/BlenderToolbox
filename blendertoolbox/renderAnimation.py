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

def renderAnimation(outputFolder, camera, duration):
    bpy.data.scenes['Scene'].render.filepath = outputFolder
    bpy.data.scenes['Scene'].camera = camera
    bpy.data.scenes['Scene'].frame_end = duration
    bpy.ops.render.render(animation = True)
