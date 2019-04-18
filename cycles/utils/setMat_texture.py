import bpy
import os

def setMat_texture(mesh, texturePath, meshColor):
    mat = bpy.data.materials.new('MeshMaterial')
    mesh.data.materials.append(mat)
    mesh.active_material = mat
    mat.use_nodes = True
    tree = mat.node_tree

    # set principled BSDF
    PRI = tree.nodes["Principled BSDF"]
    PRI.inputs['Roughness'].default_value = 0.7
    PRI.inputs['Sheen Tint'].default_value = 0

    TI = tree.nodes.new('ShaderNodeTexImage')
    TI.image = bpy.data.images.load(texturePath)
    

    # set color using Hue/Saturation node
    HSVNode = tree.nodes.new('ShaderNodeHueSaturation')
    HSVNode.inputs['Saturation'].default_value = meshColor.S
    HSVNode.inputs['Value'].default_value = meshColor.V
    HSVNode.inputs['Hue'].default_value = meshColor.H

    # set color brightness/contrast
    BCNode = tree.nodes.new('ShaderNodeBrightContrast')
    BCNode.inputs['Bright'].default_value = meshColor.B
    BCNode.inputs['Contrast'].default_value = meshColor.C

    tree.links.new(TI.outputs['Color'], HSVNode.inputs['Color'])
    tree.links.new(HSVNode.outputs['Color'], BCNode.inputs['Color'])
    tree.links.new(BCNode.outputs['Color'], PRI.inputs['Base Color'])

    # # txImg
    # TI = tree.nodes.new('ShaderNodeTexImage')
    # tree.links.new(TI.outputs['Color'], PRI.inputs['Base Color'])

    # img = bpy.data.images.load(texturePath)
    # # basename = os.path.basename(texturePath)
    # # img = bpy.data.images[basename]
    # print(img)
    # TI.image = img
    

# mat = bpy.data.materials['Material']
# tex = bpy.data.textures.new("SomeName", 'IMAGE')
# slot = mat.texture_slots.add()
# slot.texture = tex

	# # add Ambient Occlusion
	# tree.nodes.new('ShaderNodeAmbientOcclusion')
	# tree.nodes.new('ShaderNodeGamma')
	# tree.nodes.new('ShaderNodeMixRGB')
	# tree.nodes["Mix"].blend_type = 'MULTIPLY'
	# tree.nodes["Gamma"].inputs["Gamma"].default_value = AOStrength
	# tree.nodes["Ambient Occlusion"].inputs["Distance"].default_value = 10.0

	# # set color using Hue/Saturation node
	# HSVNode = tree.nodes.new('ShaderNodeHueSaturation')
	# HSVNode.inputs['Color'].default_value = meshColor.RGBA
	# HSVNode.inputs['Saturation'].default_value = meshColor.S
	# HSVNode.inputs['Value'].default_value = meshColor.V
	# HSVNode.inputs['Hue'].default_value = meshColor.H

	# # set color brightness/contrast
	# BCNode = tree.nodes.new('ShaderNodeBrightContrast')
	# BCNode.inputs['Bright'].default_value = meshColor.B
	# BCNode.inputs['Contrast'].default_value = meshColor.C

	# # link all the nodes
	# tree.links.new(HSVNode.outputs['Color'], BCNode.inputs['Color'])
	# tree.links.new(BCNode.outputs['Color'], tree.nodes['Ambient Occlusion'].inputs['Color'])
	# tree.links.new(tree.nodes["Ambient Occlusion"].outputs['Color'], tree.nodes['Mix'].inputs['Color1'])
	# tree.links.new(tree.nodes["Ambient Occlusion"].outputs['AO'], tree.nodes['Gamma'].inputs['Color'])
	# tree.links.new(tree.nodes["Gamma"].outputs['Color'], tree.nodes['Mix'].inputs['Color2'])
	# tree.links.new(tree.nodes["Mix"].outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])

	
