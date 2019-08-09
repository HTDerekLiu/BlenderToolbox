import bpy
from include import *

def drawVertexSubset(mesh, VIdx, ptSize, ptColor):
    for ii in VIdx:
        Vloc = mesh.matrix_world @ mesh.data.vertices[int(ii)].co
        bpy.ops.mesh.primitive_uv_sphere_add(radius = ptSize, location = Vloc)
        sphere = bpy.context.object
        bpy.ops.object.shade_smooth()

        mat = bpy.data.materials.new(str(ii))
        sphere.data.materials.append(mat)
        mat.use_nodes = True
        tree = mat.node_tree

        BCNode = initColorNode(tree, ptColor)

        tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 1.0
        tree.nodes["Principled BSDF"].inputs['Sheen Tint'].default_value = 0
        tree.links.new(BCNode.outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])