import bpy
from include import *

def setMat_crackedCeramic(mesh, meshColor, crackScale, crackDisp):
    mat = bpy.data.materials.new('MeshMaterial')
    mesh.data.materials.append(mat)
    mesh.active_material = mat
    mat.use_nodes = True
    tree = mat.node_tree

    # init color node
    C = initColorNode(tree, meshColor)

    GLO = tree.nodes.new('ShaderNodeBsdfGlossy')
    GLO.inputs['Roughness'].default_value = 0.316
    DIF = tree.nodes.new('ShaderNodeBsdfDiffuse')
    tree.links.new(C.outputs['Color'], DIF.inputs['Color'])

    MIXS = tree.nodes.new('ShaderNodeMixShader')
    MIXS.inputs['Fac'].default_value = 0.327
    tree.links.new(DIF.outputs['BSDF'], MIXS.inputs[1])
    tree.links.new(GLO.outputs['BSDF'], MIXS.inputs[2])

    VOR = tree.nodes.new('ShaderNodeTexVoronoi')
    VOR.inputs['Scale'].default_value = crackScale

    DISP = tree.nodes.new('ShaderNodeDisplacement')
    DISP.inputs[1].default_value = 0.0
    DISP.inputs[2].default_value = crackDisp
    tree.links.new(VOR.outputs['Fac'], DISP.inputs['Height'])
    
    tree.links.new(MIXS.outputs[0], tree.nodes['Material Output'].inputs['Surface'])
    tree.links.new(DISP.outputs[0], tree.nodes['Material Output'].inputs['Displacement'])

	
