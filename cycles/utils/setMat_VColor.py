import bpy

def setMat_VColor(mesh, \
				saturation = 1.0, \
				brightness = 1.0):
	mat = bpy.data.materials.new('MeshMaterial')
	mesh.data.materials.append(mat)
	mesh.active_material = mat
	mat.use_nodes = True
	tree = mat.node_tree

	# read vertex attribute
	tree.nodes.new('ShaderNodeAttribute')
	tree.nodes[-1].attribute_name = "Col"
	tree.nodes.new('ShaderNodeHueSaturation')
	tree.links.new(tree.nodes["Attribute"].outputs['Color'], tree.nodes['Hue Saturation Value'].inputs['Color'])
	tree.nodes["Hue Saturation Value"].inputs['Saturation'].default_value = saturation
	tree.nodes["Hue Saturation Value"].inputs['Value'].default_value = brightness

	# set principled BSDF
	tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 1.0
	tree.nodes["Principled BSDF"].inputs['Sheen Tint'].default_value = 0
	tree.links.new(tree.nodes["Hue Saturation Value"].outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])
