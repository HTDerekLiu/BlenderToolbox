import bpy

def setMat_edge(mesh, edgeThickness, edgeColor = (0,0,0,0), meshColor = (0.7,0.7,0.7,0), edgesaturation = 1.0, edgebrightness = 1.0):
	mat = bpy.data.materials.new('MeshMaterial')
	mesh.data.materials.append(mat)
	mat.use_nodes = True
	tree = mat.node_tree
	mat_mesh = tree.nodes["Diffuse BSDF"]
	mat_mesh.inputs['Color'].default_value = meshColor
	tree.nodes.new(type="ShaderNodeWireframe")
	wire = tree.nodes[-1]
	tree.nodes.new(type="ShaderNodeBsdfDiffuse")
	mat_wire = tree.nodes[-1]
	tree.nodes.new('ShaderNodeMixShader')
	tree.links.new(wire.outputs[0], tree.nodes['Mix Shader'].inputs[0])
	tree.links.new(mat_wire.outputs['BSDF'], tree.nodes['Mix Shader'].inputs[2])
	tree.links.new(mat_mesh.outputs['BSDF'], tree.nodes['Mix Shader'].inputs[1])
	tree.links.new(tree.nodes["Mix Shader"].outputs['Shader'], tree.nodes['Material Output'].inputs['Surface'])
	wire.inputs[0].default_value = edgeThickness
	tree.nodes.new('ShaderNodeHueSaturation')
	tree.links.new(tree.nodes["Hue Saturation Value"].outputs['Color'],mat_wire.inputs['Color'])
	tree.nodes["Hue Saturation Value"].inputs['Color'].default_value = edgeColor
	tree.nodes["Hue Saturation Value"].inputs['Saturation'].default_value = edgesaturation
	tree.nodes["Hue Saturation Value"].inputs['Value'].default_value = edgebrightness