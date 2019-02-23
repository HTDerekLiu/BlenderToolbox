import bpy

def setMat_transparent(mesh, saturation = 1.0, brightness = 1.0, meshColor = (1,1,1,1), tranaparency = 0.9):
	mat = bpy.data.materials.new('MeshMaterial')
	mesh.data.materials.append(mat)
	mat.use_nodes = True
	tree = mat.node_tree
	tree.nodes.new('ShaderNodeBsdfTransparent')
	tree.nodes.new('ShaderNodeMixShader')
	tree.nodes.new('ShaderNodeHueSaturation')
	tree.links.new(tree.nodes["Diffuse BSDF"].outputs['BSDF'], tree.nodes['Mix Shader'].inputs[1])
	tree.links.new(tree.nodes["Transparent BSDF"].outputs['BSDF'], tree.nodes['Mix Shader'].inputs[2])
	tree.links.new(tree.nodes["Mix Shader"].outputs['Shader'], tree.nodes['Material Output'].inputs['Surface'])
	tree.links.new(tree.nodes["Hue Saturation Value"].outputs['Color'], tree.nodes['Diffuse BSDF'].inputs['Color'])

	tree.nodes["Mix Shader"].inputs['Fac'].default_value = tranaparency
	tree.nodes["Transparent BSDF"].inputs['Color'].default_value = meshColor
	tree.nodes["Diffuse BSDF"].inputs['Color'].default_value = meshColor
	tree.nodes["Hue Saturation Value"].inputs['Color'].default_value = meshColor
	tree.nodes["Hue Saturation Value"].inputs['Saturation'].default_value = saturation
	tree.nodes["Hue Saturation Value"].inputs['Value'].default_value = brightness