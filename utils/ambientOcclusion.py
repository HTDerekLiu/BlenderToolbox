import bpy

def ambientOcclusion(AOStrength = 1.5):
	scene = bpy.data.scenes[0]
	scene.use_nodes = True
	scene.render.layers[0].use_pass_ambient_occlusion = True
	tree = scene.node_tree
	tree.nodes.new(type = 'CompositorNodeGamma')
	gamma = tree.nodes[-1]
	rendLayer = tree.nodes["Render Layers"]
	tree.links.new(rendLayer.outputs["AO"], gamma.inputs[0])
	tree.nodes.new(type = 'CompositorNodeMixRGB')
	mix = tree.nodes[-1]
	mix.blend_type = "MULTIPLY"
	tree.links.new(gamma.outputs[0], mix.inputs[2])
	tree.links.new(rendLayer.outputs["Image"], mix.inputs[1])
	tree.links.new(mix.outputs[0], tree.nodes["Composite"].inputs[0])

	mix.inputs[0].default_value = 1.0
	gamma.inputs[1].default_value = AOStrength