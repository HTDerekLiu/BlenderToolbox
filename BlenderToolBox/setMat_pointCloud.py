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

def setMat_pointCloud(mesh, \
                meshColor, \
                ptSize, \
                AOStrength = 0.0): 
    # set the material of the point cloud (single color here)
    mat = bpy.data.materials.new('MeshMaterial')
    mat.use_nodes = True
    tree = mat.node_tree

    # set principled BSDF
    tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.7
    tree.nodes["Principled BSDF"].inputs['Sheen Tint'].default_value = 0

    # add Ambient Occlusion
    tree.nodes.new('ShaderNodeAmbientOcclusion')
    tree.nodes.new('ShaderNodeGamma')
    tree.nodes.new('ShaderNodeMixRGB')
    tree.nodes["Mix"].blend_type = 'MULTIPLY'
    tree.nodes["Gamma"].inputs["Gamma"].default_value = AOStrength
    tree.nodes["Ambient Occlusion"].inputs["Distance"].default_value = 10.0
    tree.nodes["Gamma"].location.x -= 600

    # set color using Hue/Saturation node
    HSVNode = tree.nodes.new('ShaderNodeHueSaturation')
    HSVNode.inputs['Color'].default_value = meshColor.RGBA
    HSVNode.inputs['Saturation'].default_value = meshColor.S
    HSVNode.inputs['Value'].default_value = meshColor.V
    HSVNode.inputs['Hue'].default_value = meshColor.H
    HSVNode.location.x -= 200

    # set color brightness/contrast
    BCNode = tree.nodes.new('ShaderNodeBrightContrast')
    BCNode.inputs['Bright'].default_value = meshColor.B
    BCNode.inputs['Contrast'].default_value = meshColor.C
    BCNode.location.x -= 400

    # link all the nodes
    tree.links.new(HSVNode.outputs['Color'], BCNode.inputs['Color'])
    tree.links.new(BCNode.outputs['Color'], tree.nodes['Ambient Occlusion'].inputs['Color'])
    tree.links.new(tree.nodes["Ambient Occlusion"].outputs['Color'], tree.nodes['Mix'].inputs['Color1'])
    tree.links.new(tree.nodes["Ambient Occlusion"].outputs['AO'], tree.nodes['Gamma'].inputs['Color'])
    tree.links.new(tree.nodes["Gamma"].outputs['Color'], tree.nodes['Mix'].inputs['Color2'])
    tree.links.new(tree.nodes["Mix"].outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])

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


    # # initialize a primitive sphere
    # bpy.ops.mesh.primitive_uv_sphere_add(radius = 1.0, location = (1e7,1e7,1e7))
    # sphere = bpy.context.object
    # bpy.ops.object.shade_smooth()
    # mat = bpy.data.materials.new(name="sphereMat")
    # sphere.data.materials.append(mat)
    # sphere.active_material = mat
    # mat.use_nodes = True
    # tree = mat.node_tree
    # HSVNode = tree.nodes.new('ShaderNodeHueSaturation')
    # HSVNode.inputs['Color'].default_value = ptColor.RGBA
    # HSVNode.inputs['Saturation'].default_value = ptColor.S
    # HSVNode.inputs['Value'].default_value = ptColor.V
    # HSVNode.inputs['Hue'].default_value = ptColor.H

    # # set color brightness/contrast
    # BCNode = tree.nodes.new('ShaderNodeBrightContrast')
    # BCNode.inputs['Bright'].default_value = ptColor.B
    # BCNode.inputs['Contrast'].default_value = ptColor.C
    # tree.links.new(HSVNode.outputs['Color'], BCNode.inputs['Color'])
    # tree.links.new(BCNode.outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])

    # # init particle system
    # mesh.modifiers.new("part", type='PARTICLE_SYSTEM')
    # ps = mesh.particle_systems[0]
    # ps.settings.count = len(mesh.data.vertices)
    # ps.settings.frame_start = 0
    # ps.settings.frame_end = 0
    # ps.settings.emit_from = 'VERT'
    # ps.settings.physics_type = 'NO'
    # ps.settings.particle_size = ptSize
    # ps.settings.render_type = 'OBJECT'
    # ps.settings.instance_object = sphere
    # ps.settings.use_emit_random = False

