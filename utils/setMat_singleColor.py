import bpy

def setMat_singleColor(mesh, saturation = 1.0, brightness = 0.8, meshColor = (144.0/255.0, 210.0/255.0, 236.0/255.0,0), AOStrength = 1.0):
	mat = bpy.data.materials.new('MeshMaterial')
	mesh.data.materials.append(mat)
	mesh.active_material = mat
	mat.use_nodes = True
	tree = mat.node_tree

	# set principled BSDF
	tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.7
	tree.nodes["Principled BSDF"].inputs['Sheen Tint'].default_value = 0

	# add Ambient Occlusion
	tree.nodes.new('ShaderNodeAmbientOcclusion')
	tree.nodes.new('ShaderNodeGamma')
	tree.nodes.new('ShaderNodeMixRGB')
	tree.nodes["Mix"].blend_type = 'MULTIPLY'
	tree.nodes["Gamma"].inputs["Gamma"].default_value = AOStrength
	tree.nodes["Ambient Occlusion"].inputs["Distance"].default_value = 10.0

	# set color using Hue/Saturation node
	tree.nodes.new('ShaderNodeHueSaturation')
	tree.nodes["Hue Saturation Value"].inputs['Color'].default_value = meshColor
	tree.nodes["Hue Saturation Value"].inputs['Saturation'].default_value = saturation
	tree.nodes["Hue Saturation Value"].inputs['Value'].default_value = brightness

	# link all the nodes
	tree.links.new(tree.nodes["Hue Saturation Value"].outputs['Color'], tree.nodes['Ambient Occlusion'].inputs['Color'])
	tree.links.new(tree.nodes["Ambient Occlusion"].outputs['Color'], tree.nodes['Mix'].inputs['Color1'])
	tree.links.new(tree.nodes["Ambient Occlusion"].outputs['AO'], tree.nodes['Gamma'].inputs['Color'])
	tree.links.new(tree.nodes["Gamma"].outputs['Color'], tree.nodes['Mix'].inputs['Color2'])
	tree.links.new(tree.nodes["Mix"].outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])

	
