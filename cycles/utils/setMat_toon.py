import bpy
import numpy as np

def setMat_toon(mesh, \
            meshColor, \
            saturation, \
            brightness, \
            colorPos = (0.05, 0.15),\
            hsv_Vrange = (0.6,0.0)):
    mat = bpy.data.materials.new('MeshMaterial')
    mesh.data.materials.append(mat)
    mesh.active_material = mat
    mat.use_nodes = True
    tree = mat.node_tree

    numColor = len(colorPos) + 1 # colorPos >= 2
    C = np.linspace(hsv_Vrange[0], hsv_Vrange[1], num=numColor) 

    # init level
    initRGB = tree.nodes.new('ShaderNodeHueSaturation')
    initRGB.inputs['Color'].default_value = (.5,.5,.5,1)
    initRGB.inputs['Hue'].default_value = 0
    initRGB.inputs['Saturation'].default_value = 0
    initRGB.inputs['Value'].default_value = C[0]

    # init array
    RGBList = [None] * (numColor - 1)
    RampList = [None] * (numColor - 1)
    MixList = [None] * (numColor - 1)
    for ii in range(numColor-1):
        # RGB node
        RGBList[ii] = tree.nodes.new('ShaderNodeHueSaturation')
        RGBList[ii].inputs['Color'].default_value = (.5,.5,.5,1)
        RGBList[ii].inputs['Hue'].default_value = 0
        RGBList[ii].inputs['Saturation'].default_value = 0
        RGBList[ii].inputs['Value'].default_value = C[ii+1]
        # Color Ramp
        RampList[ii] = tree.nodes.new('ShaderNodeValToRGB')
        RampList[ii].color_ramp.interpolation = 'CONSTANT'
        RampList[ii].color_ramp.elements[1].position = colorPos[ii]
        # Mix shader
        MixList[ii] = tree.nodes.new('ShaderNodeMixShader')
        # Link shaders
        if ii > 0 and ii < (numColor-1):
            tree.links.new(MixList[ii-1].outputs['Shader'], MixList[ii].inputs[1])
        tree.links.new(RampList[ii].outputs['Color'], MixList[ii].inputs[0])
        tree.links.new(RGBList[ii].outputs['Color'], MixList[ii].inputs[2])

    # color of the mesh
    mainColor = tree.nodes.new('ShaderNodeHueSaturation')
    mainColor.inputs['Color'].default_value = meshColor
    mainColor.inputs['Saturation'].default_value = saturation
    mainColor.inputs['Value'].default_value = brightness

    # initial and end links
    addShader = tree.nodes.new('ShaderNodeAddShader')
    tree.links.new(initRGB.outputs['Color'], MixList[0].inputs[1])
    tree.links.new(MixList[-1].outputs['Shader'], addShader.inputs[0])
    tree.links.new(mainColor.outputs['Color'], addShader.inputs[1])
    tree.links.new(addShader.outputs['Shader'], tree.nodes['Material Output'].inputs['Surface'])

    # add normal to the color
    fresnelNode = tree.nodes.new('ShaderNodeFresnel')
    textureNode = tree.nodes.new('ShaderNodeTexCoord')
    tree.links.new(textureNode.outputs['Normal'], fresnelNode.inputs['Normal'])
    for ii in range(len(RampList)):
        tree.links.new(fresnelNode.outputs[0], RampList[ii].inputs['Fac'])