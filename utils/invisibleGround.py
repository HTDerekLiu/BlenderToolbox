import bpy

def invisibleGround(location = (0,0,0), radius = 5, shadowDarkeness = 0.18):
	# initialize a ground for shadow
	bpy.context.scene.cycles.film_transparent = True
	bpy.ops.mesh.primitive_plane_add(location = location, radius = radius)
	bpy.context.object.cycles.is_shadow_catcher = True

	# set material
	ground = bpy.context.object
	mat = bpy.data.materials.new('MeshMaterial')
	ground.data.materials.append(mat)
	mat.use_nodes = True
	tree = mat.node_tree
	tree.nodes.new('ShaderNodeMixShader')
	tree.nodes.new('ShaderNodeBsdfGlass')
	tree.links.new(tree.nodes["Diffuse BSDF"].outputs['BSDF'], tree.nodes['Mix Shader'].inputs[2])
	tree.links.new(tree.nodes["Glass BSDF"].outputs['BSDF'], tree.nodes['Mix Shader'].inputs[1])
	tree.links.new(tree.nodes["Mix Shader"].outputs['Shader'], tree.nodes['Material Output'].inputs['Surface'])
	tree.nodes["Diffuse BSDF"].inputs['Color'].default_value = (1,1,1,1)
	tree.nodes["Glass BSDF"].inputs['Color'].default_value = (1,1,1,1)
	tree.nodes["Glass BSDF"].inputs[1].default_value = 1.0
	tree.nodes["Glass BSDF"].inputs[2].default_value = 1.0
	tree.nodes["Mix Shader"].inputs['Fac'].default_value = shadowDarkeness