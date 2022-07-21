# Copyright 2020 Hsueh-Ti Derek Liu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import bpy
from mathutils import Vector

def setMat_pointCloudColored(mesh, meshColor, ptSize): 
    mat = bpy.data.materials.new('MeshMaterial')
    mesh.data.materials.append(mat)
    mesh.active_material = mat
    mat.use_nodes = True
    tree = mat.node_tree

    # read vertex attribute
    tree.nodes.new('ShaderNodeAttribute')
    tree.nodes[-1].attribute_name = "Col"
    HSVNode = tree.nodes.new('ShaderNodeHueSaturation')
    tree.links.new(tree.nodes["Attribute"].outputs['Color'], HSVNode.inputs['Color'])
    HSVNode.inputs['Saturation'].default_value = meshColor.S
    HSVNode.inputs['Value'].default_value = meshColor.V
    HSVNode.inputs['Hue'].default_value = meshColor.H
    HSVNode.location.x -= 200

    # set color brightness/contrast
    BCNode = tree.nodes.new('ShaderNodeBrightContrast')
    BCNode.inputs['Bright'].default_value = meshColor.B
    BCNode.inputs['Contrast'].default_value = meshColor.C
    BCNode.location.x -= 400

    # set principled BSDF
    tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 1.0
    tree.nodes["Principled BSDF"].inputs['Sheen Tint'].default_value = 0
    tree.links.new(HSVNode.outputs['Color'], BCNode.inputs['Color'])
    tree.links.new(BCNode.outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])

    # turn a mesh into point cloud using geometry node
    mesh.select_set(True)
    bpy.context.view_layer.objects.active = mesh

    # this if else is a quick hack to handle blender 3.2.x vs earlier versions
    bpy.ops.object.modifier_add(type='NODES')
    if mesh.modifiers[-1].node_group:
        geo_tree = mesh.modifiers[-1].node_group    
    else:
        geo_tree = new_GeometryNodes_group()
        mesh.modifiers[-1].node_group = geo_tree
    IN = geo_tree.nodes['Group Input']
    OUT = geo_tree.nodes['Group Output']
    MESH2POINT = geo_tree.nodes.new('GeometryNodeMeshToPoints')
    MESH2POINT.location.x -= 100
    MESH2POINT.inputs['Radius'].default_value = ptSize
    MATERIAL = geo_tree.nodes.new('GeometryNodeSetMaterial')

    geo_tree.links.new(IN.outputs['Geometry'], MESH2POINT.inputs['Mesh'])
    geo_tree.links.new(MESH2POINT.outputs['Points'], MATERIAL.inputs['Geometry'])
    geo_tree.links.new(MATERIAL.outputs['Geometry'], OUT.inputs['Geometry'])

    # assign the material to point cloud
    MATERIAL.inputs[2].default_value = mat

def new_GeometryNodes_group():
    ''' Create a new empty node group that can be used
        in a GeometryNodes modifier.
    '''
    node_group = bpy.data.node_groups.new('GeometryNodes', 'GeometryNodeTree')
    inNode = node_group.nodes.new('NodeGroupInput')
    inNode.outputs.new('NodeSocketGeometry', 'Geometry')
    outNode = node_group.nodes.new('NodeGroupOutput')
    outNode.inputs.new('NodeSocketGeometry', 'Geometry')
    node_group.links.new(inNode.outputs['Geometry'], outNode.inputs['Geometry'])
    inNode.location = Vector((-1.5*inNode.width, 0))
    outNode.location = Vector((1.5*outNode.width, 0))
    return node_group