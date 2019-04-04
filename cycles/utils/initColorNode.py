import bpy

def initColorNode(tree, color):
    HSV = tree.nodes.new('ShaderNodeHueSaturation')
    HSV.inputs['Color'].default_value = color.RGBA
    HSV.inputs['Saturation'].default_value = color.S
    HSV.inputs['Value'].default_value = color.V
    HSV.inputs['Hue'].default_value = color.H
    BS = tree.nodes.new('ShaderNodeBrightContrast')
    BS.inputs['Bright'].default_value = color.B
    BS.inputs['Contrast'].default_value = color.C
    tree.links.new(HSV.outputs['Color'], BS.inputs['Color'])
    return BS