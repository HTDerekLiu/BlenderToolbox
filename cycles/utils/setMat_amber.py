import bpy

def setMat_amber(mesh, meshColor):
    mat = bpy.data.materials.new('MeshMaterial')
    mesh.data.materials.append(mat)
    mesh.active_material = mat
    mat.use_nodes = True
    tree = mat.node_tree

    # init color node
    HSVNode = tree.nodes.new('ShaderNodeHueSaturation')
    HSVNode.inputs['Color'].default_value = meshColor.RGBA
    HSVNode.inputs['Saturation'].default_value = meshColor.S
    HSVNode.inputs['Value'].default_value = meshColor.V
    HSVNode.inputs['Hue'].default_value = meshColor.H
    BCNode = tree.nodes.new('ShaderNodeBrightContrast')
    BCNode.inputs['Bright'].default_value = meshColor.B
    BCNode.inputs['Contrast'].default_value = meshColor.C
    tree.links.new(HSVNode.outputs['Color'], BCNode.inputs['Color'])

    # construct amber node
    fresnel = tree.nodes.new('ShaderNodeFresnel')
    fresnel.inputs[0].default_value = 1.3

    glass = tree.nodes.new('ShaderNodeBsdfGlass')
    tree.links.new(BCNode.outputs['Color'], glass.inputs['Color'])

    transparent = tree.nodes.new('ShaderNodeBsdfTransparent')
    tree.links.new(BCNode.outputs['Color'], transparent.inputs['Color'])

    multiply = tree.nodes.new('ShaderNodeMixRGB')
    multiply.blend_type = 'MULTIPLY'
    multiply.inputs['Fac'].default_value = 1
    multiply.inputs['Color2'].default_value = (1,1,1,1)
    tree.links.new(fresnel.outputs['Fac'], multiply.inputs['Color1'])

    mix1 = tree.nodes.new('ShaderNodeMixShader')
    mix1.inputs['Fac'].default_value = 0.7
    tree.links.new(glass.outputs[0], mix1.inputs[1])
    tree.links.new(transparent.outputs[0], mix1.inputs[2])

    glossy = tree.nodes.new('ShaderNodeBsdfGlossy')
    glossy.inputs['Color'].default_value = (0.8, 0.72, 0.437, 1)

    mix2 = tree.nodes.new('ShaderNodeMixShader')
    tree.links.new(multiply.outputs[0], mix2.inputs[0])
    tree.links.new(mix1.outputs[0], mix2.inputs[1])
    tree.links.new(glossy.outputs[0], mix2.inputs[2])

    tree.links.new(mix2.outputs[0], tree.nodes['Material Output'].inputs['Surface'])

	
