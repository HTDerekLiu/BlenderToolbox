import bpy

def setMat_VColor(mesh, saturation = 1.0):
	mat = bpy.data.materials.new('MeshMaterial')
	mesh.data.materials.append(mat)
	mat.use_nodes = True
	tree = mat.node_tree
	tree.nodes.new('ShaderNodeAttribute')
	tree.nodes[-1].attribute_name = "Col"
	tree.nodes.new('ShaderNodeBsdfGlossy')
	tree.nodes.new('ShaderNodeMixShader')
	tree.nodes.new('ShaderNodeHueSaturation')
	tree.links.new(tree.nodes["Attribute"].outputs['Color'], tree.nodes['Hue Saturation Value'].inputs['Color'])
	tree.links.new(tree.nodes["Diffuse BSDF"].outputs['BSDF'], tree.nodes['Mix Shader'].inputs[1])
	tree.links.new(tree.nodes["Glossy BSDF"].outputs['BSDF'], tree.nodes['Mix Shader'].inputs[2])
	tree.links.new(tree.nodes["Mix Shader"].outputs['Shader'], tree.nodes['Material Output'].inputs['Surface'])
	tree.links.new(tree.nodes["Hue Saturation Value"].outputs['Color'], tree.nodes['Diffuse BSDF'].inputs['Color'])
	tree.links.new(tree.nodes["Hue Saturation Value"].outputs['Color'], tree.nodes['Glossy BSDF'].inputs['Color'])
	tree.nodes["Mix Shader"].inputs['Fac'].default_value = 0.2
	tree.nodes["Glossy BSDF"].inputs[1].default_value = 0.4
	tree.nodes["Hue Saturation Value"].inputs['Saturation'].default_value = saturation
	tree.nodes["Hue Saturation Value"].inputs['Value'].default_value = 1.3