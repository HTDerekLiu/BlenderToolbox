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
import os

def readImagePlane(imagePath, location, rotation_euler, radius, brightness):
	x = rotation_euler[0] * 1.0 / 180.0 * np.pi 
	y = rotation_euler[1] * 1.0 / 180.0 * np.pi 
	z = rotation_euler[2] * 1.0 / 180.0 * np.pi 
	angle = (x,y,z)

	# load image
	imageData = bpy.data.images.load(os.path.abspath(imagePath))
	w = imageData.size[0]
	h = imageData.size[1]
	ratio = h*1.0/w

	# create image plane
	bpy.ops.mesh.primitive_plane_add(location = location, size = radius, rotation=angle)
	mesh = bpy.context.selected_objects[0]
	mesh.scale = (1.0, ratio, 1.0)

	# set material
	mat = bpy.data.materials.new('MeshMaterial')
	mesh.data.materials.append(mat)
	mesh.active_material = mat
	mat.use_nodes = True
	tree = mat.node_tree

	TI = tree.nodes.new('ShaderNodeTexImage')
	TI.image = imageData

	EM = tree.nodes.new('ShaderNodeEmission')
	EM.inputs[1].default_value = brightness

	tree.links.new(TI.outputs['Color'], EM.inputs['Color'])
	tree.links.new(EM.outputs[0], tree.nodes['Material Output'].inputs['Surface'])

	return mesh