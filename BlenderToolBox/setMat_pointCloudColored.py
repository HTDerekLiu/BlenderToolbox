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

def setMat_pointCloudColored(mesh, meshColor, ptSize): 
    mat = bpy.data.materials.new('MeshMaterial')
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

    bpy.ops.object.modifier_add(type='NODES')
    tree = mesh.modifiers[-1].node_group
    IN = tree.nodes['Group Input']
    OUT = tree.nodes['Group Output']
    MESH2POINT = tree.nodes.new('GeometryNodeMeshToPoints')
    MESH2POINT.location.x -= 100
    MESH2POINT.inputs['Radius'].default_value = ptSize
    MATERIAL = tree.nodes.new('GeometryNodeSetMaterial')

    tree.links.new(IN.outputs['Geometry'], MESH2POINT.inputs['Mesh'])
    tree.links.new(MESH2POINT.outputs['Points'], MATERIAL.inputs['Geometry'])
    tree.links.new(MATERIAL.outputs['Geometry'], OUT.inputs['Geometry'])

    # assign the material to point cloud
    MATERIAL.inputs[2].default_value = mat