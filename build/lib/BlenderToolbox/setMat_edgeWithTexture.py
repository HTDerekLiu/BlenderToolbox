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
import bpy, os

def setMat_edgeWithTexture(mesh, edgeThickness, edgeRGBA, texturePath, textureHSVBC):

	meshRGBA = (1,1,1,0)

	# initialize material node graph
	mat = bpy.data.materials.new('MeshMaterial')
	mesh.data.materials.append(mat)
	mesh.active_material = mat
	mat.use_nodes = True
	tree = mat.node_tree

	# add edge wire rendering
	WIRE_RGB = tree.nodes.new('ShaderNodeRGB')
	WIRE_RGB.outputs[0].default_value = edgeRGBA
	WIRE_RGB.location.x -= 200
	WIRE_RGB.location.y -= 400

	WIRE = tree.nodes.new(type="ShaderNodeWireframe")
	WIRE.inputs[0].default_value = edgeThickness
	WIRE.location.x -= 200
	WIRE.location.y += 200

	MIX = tree.nodes.new('ShaderNodeMixRGB')
	MIX.blend_type = 'MIX'
	
	# add texture
	TI = tree.nodes.new('ShaderNodeTexImage')
	absTexturePath = os.path.abspath(texturePath)
	TI.image = bpy.data.images.load(absTexturePath)
	TI.location.x -= 700

	# set color using Hue/Saturation node
	HSVNode = tree.nodes.new('ShaderNodeHueSaturation')
	HSVNode.inputs['Saturation'].default_value = textureHSVBC.S
	HSVNode.inputs['Value'].default_value = textureHSVBC.V
	HSVNode.inputs['Hue'].default_value = textureHSVBC.H
	HSVNode.location.x -= 400

	# set color brightness/contrast
	BCNode = tree.nodes.new('ShaderNodeBrightContrast')
	BCNode.inputs['Bright'].default_value = textureHSVBC.B
	BCNode.inputs['Contrast'].default_value = textureHSVBC.C
	BCNode.location.x -= 200

	# set principled BSDF
	PRI = tree.nodes["Principled BSDF"]
	PRI.inputs['Roughness'].default_value = 0.3
	PRI.inputs['Sheen Tint'].default_value = [0, 0, 0, 1]
	PRI.inputs['Specular IOR Level'].default_value = 0.2
	PRI.inputs['IOR'].default_value = 1.45
	PRI.inputs['Transmission Weight'].default_value = 0
	PRI.inputs['Coat Roughness'].default_value = 0


	# link everything
	tree.links.new(BCNode.outputs['Color'], PRI.inputs['Base Color'])
	tree.links.new(TI.outputs['Color'], HSVNode.inputs['Color'])
	tree.links.new(HSVNode.outputs['Color'], BCNode.inputs['Color'])
	tree.links.new(BCNode.outputs['Color'], MIX.inputs[1])
	tree.links.new(WIRE.outputs[0], MIX.inputs[0])
	tree.links.new(WIRE_RGB.outputs[0], MIX.inputs[2])
	tree.links.new(MIX.outputs[0], PRI.inputs[0])
	tree.links.new(PRI.outputs[0], tree.nodes['Material Output'].inputs['Surface'])


