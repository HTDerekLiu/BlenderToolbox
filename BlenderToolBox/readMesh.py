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
import bmesh
import os
from .readOBJ import readOBJ
from .readPLY import readPLY
from .readSTL import readSTL

def readMesh(filePath, location, rotation_euler, scale):
	_, extension = os.path.splitext(filePath)
	if extension == '.ply' or extension == '.PLY':
		mesh = readPLY(filePath, location, rotation_euler, scale)
	elif extension == '.obj' or extension == '.OBJ':
		mesh = readOBJ(filePath, location, rotation_euler, scale)
	elif extension == '.stl' or extension == '.STL':
	 	mesh = readSTL(filePath, location, rotation_euler, scale)
	else:
		raise TypeError("only support .ply, .obj, and .stl for now")
	bpy.context.view_layer.objects.active = mesh
	bpy.ops.object.shade_flat() # defaiult flat shading
	return mesh 