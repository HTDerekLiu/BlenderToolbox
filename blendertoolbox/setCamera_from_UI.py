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

def setCamera_from_UI(camLocation, rotation_euler, focalLength = 35):
	# initialize camera
	bpy.ops.object.camera_add(location = camLocation) # name 'Camera'
	cam = bpy.context.object
	cam.data.lens = focalLength
	cam.rotation_euler[0] = rotation_euler[0] * 1.0 / 180.0 * np.pi
	cam.rotation_euler[1] = rotation_euler[1] * 1.0 / 180.0 * np.pi
	cam.rotation_euler[2] = rotation_euler[2] * 1.0 / 180.0 * np.pi
	return cam