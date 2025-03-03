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

def setMat_ambient_occlusion(mesh, distance = 10.0, samples = 16):
	mat = bpy.data.materials.new('MeshMaterial')
	mesh.data.materials.append(mat)
	mesh.active_material = mat
	mat.use_nodes = True
	tree = mat.node_tree

	# set principled BSDF
	tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.3
	tree.nodes["Principled BSDF"].inputs['Sheen Tint'].default_value = [0, 0, 0, 1]
	tree.nodes["Principled BSDF"].inputs['Specular IOR Level'].default_value = 0.5
	tree.nodes["Principled BSDF"].inputs['IOR'].default_value = 1.45
	tree.nodes["Principled BSDF"].inputs['Transmission Weight'].default_value = 0
	tree.nodes["Principled BSDF"].inputs['Coat Roughness'].default_value = 0

	# add Ambient Occlusion
	AONode = tree.nodes.new('ShaderNodeAmbientOcclusion')
	AONode.inputs["Distance"].default_value = distance
	AONode.samples = samples
	tree.links.new(AONode.outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])

	
