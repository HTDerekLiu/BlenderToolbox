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

def setMat_honey(mesh, meshColor, notTransparency = 0.6):
	mat = bpy.data.materials.new('MeshMaterial')
	mesh.data.materials.append(mat)
	mesh.active_material = mat
	mat.use_nodes = True
	tree = mat.node_tree

	# set principled BSDF
	tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.7
	tree.nodes["Principled BSDF"].inputs['Sheen Tint'].default_value = [0, 0, 0, 1]

	MIXNode = tree.nodes.new('ShaderNodeMixShader')
	MIXNode.inputs[0].default_value = notTransparency

	TLNode = tree.nodes.new('ShaderNodeBsdfTranslucent')
	TPNode = tree.nodes.new('ShaderNodeBsdfTransparent')

	# set color using Hue/Saturation node
	HSVNode = tree.nodes.new('ShaderNodeHueSaturation')
	HSVNode.inputs['Color'].default_value = meshColor.RGBA
	HSVNode.inputs['Saturation'].default_value = meshColor.S
	HSVNode.inputs['Value'].default_value = meshColor.V
	HSVNode.inputs['Hue'].default_value = meshColor.H
	HSVNode.location.x -= 200

	# set color brightness/contrast
	BCNode = tree.nodes.new('ShaderNodeBrightContrast')
	BCNode.inputs['Bright'].default_value = meshColor.B
	BCNode.inputs['Contrast'].default_value = meshColor.C
	BCNode.location.x -= 400

	tree.links.new(HSVNode.outputs['Color'], BCNode.inputs['Color'])
	tree.links.new(BCNode.outputs['Color'], TLNode.inputs['Color'])

	tree.links.new(TPNode.outputs[0], MIXNode.inputs[1])
	tree.links.new(TLNode.outputs[0], MIXNode.inputs[2])
	tree.links.new(MIXNode.outputs[0], tree.nodes['Material Output'].inputs['Surface'])
	
