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

def setMat_balloon(mesh, meshColor, AOStrength = 0.0):
	# reference: https://www.youtube.com/watch?v=8KZ6M-FeC8g

	mat = bpy.data.materials.new('MeshMaterial')
	mesh.data.materials.append(mat)
	mesh.active_material = mat
	mat.use_nodes = True
	tree = mat.node_tree

	# set principled BSDF
	tree.nodes["Principled BSDF"].inputs['Specular IOR Level'].default_value = 0.5
	tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.3
	tree.nodes["Principled BSDF"].inputs['Sheen Tint'].default_value = [0.5, 0.5, 0.5, 1] # expects a sequence now
	tree.nodes["Principled BSDF"].inputs['Coat Roughness'].default_value = 0.3
	tree.nodes["Principled BSDF"].inputs['Coat Weight'].default_value = 1

	# add Ambient Occlusion
	tree.nodes.new('ShaderNodeAmbientOcclusion')
	tree.nodes.new('ShaderNodeGamma')
	tree.nodes.new('ShaderNodeMixRGB')
	tree.nodes["Mix (Legacy)"].blend_type = 'MULTIPLY'
	tree.nodes["Gamma"].inputs["Gamma"].default_value = AOStrength
	tree.nodes["Ambient Occlusion"].inputs["Distance"].default_value = 10.0
	tree.nodes["Gamma"].location.x -= 600

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

	# link all the nodes
	tree.links.new(HSVNode.outputs['Color'], BCNode.inputs['Color'])
	tree.links.new(BCNode.outputs['Color'], tree.nodes['Ambient Occlusion'].inputs['Color'])
	tree.links.new(tree.nodes["Ambient Occlusion"].outputs['Color'], tree.nodes['Mix (Legacy)'].inputs['Color1'])
	tree.links.new(tree.nodes["Ambient Occlusion"].outputs['AO'], tree.nodes['Gamma'].inputs['Color'])
	tree.links.new(tree.nodes["Gamma"].outputs['Color'], tree.nodes['Mix (Legacy)'].inputs['Color2'])
	tree.links.new(tree.nodes["Mix (Legacy)"].outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])

	# add transparent
	TRAN = tree.nodes.new('ShaderNodeBsdfTransparent')
	MIX = tree.nodes.new('ShaderNodeMixShader')
	MIX2 = tree.nodes.new('ShaderNodeMixShader')
	MIX2.inputs[0].default_value = 0.2
	LAY = tree.nodes.new('ShaderNodeLayerWeight')
	LAY.inputs[0].default_value = 0.3
	DIF = tree.nodes.new('ShaderNodeBsdfDiffuse')



	PRIN = tree.nodes["Principled BSDF"]
	tree.links.new(PRIN.outputs[0], MIX.inputs[2])
	tree.links.new(TRAN.outputs[0], MIX2.inputs[1])
	tree.links.new(TRAN.outputs[0], MIX2.inputs[2])
	tree.links.new(DIF.outputs[0], MIX2.inputs[1])
	tree.links.new(LAY.outputs[1], MIX.inputs[0])
	tree.links.new(MIX2.outputs[0], MIX.inputs[1])
	tree.links.new(tree.nodes["Mix (Legacy)"].outputs['Color'], TRAN.inputs[0])
	tree.links.new(tree.nodes["Mix (Legacy)"].outputs['Color'], DIF.inputs[0])
	tree.links.new(MIX.outputs[0], tree.nodes['Material Output'].inputs['Surface'])

	