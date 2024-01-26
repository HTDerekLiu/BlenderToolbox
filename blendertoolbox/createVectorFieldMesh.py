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
import bpy, bmesh
import numpy as np
import math

# TODO: for some reasons, I cannot use python to link face area to scale the arrows
def createVectorFieldMesh(P, PN, thickness, length, location, rotation, scale):
    # create a reference arroa mesh
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1))
    arrow_obj = bpy.data.objects[-1]
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center = 'MEDIAN') # set the object origin to the bottom
    bpy.ops.object.editmode_toggle()
    arrow_bmesh = bmesh.from_edit_mesh(arrow_obj.data)
    vertices= [v for v in arrow_bmesh.verts]
    for v in vertices:
        if v.index == 81: # 81 is the vertex index for the top UV sphere
            bpy.ops.mesh.select_all(action = 'DESELECT')
            v.select = True
            bpy.ops.transform.translate(value = (0,0,1),constraint_axis = (False, False, True),orient_type = 'GLOBAL',use_proportional_edit=True, proportional_edit_falloff='LINEAR')
    bpy.ops.object.editmode_toggle()
    # arrow_obj.scale = arrow_scale # scale it so that it looks more like an needle
    arrow_obj.location = (1e5,1e5,1e5) # move it out of the scene
    bpy.ops.object.shade_smooth()

    # create a triangle mesh for point cloud (V,F)
    x = np.random.rand(PN.shape[0],3)
    PN_normalized = PN / np.sqrt(np.sum(PN*PN,1))[:,None]
    x -= np.sum(x*PN_normalized,1)[:,None] * PN_normalized 
    x = x / np.sqrt(np.sum(x*x, 1))[:,None] * 1e-4
    y =  np.cross(PN_normalized, x)
    y = y / np.sqrt(np.sum(y*y, 1))[:,None] * 1e-3
    V0 = P + 0.5 * x - np.sqrt(3)/4. * y
    V1 = P + np.sqrt(3)/4. * y
    V2 = P - 0.5 * x - np.sqrt(3)/4. * y
    V = np.vstack((V0,V1,V2))
    F = np.arange(V.shape[0]).reshape(3,-1).T

    # set location  rotation scalig for he quad mesh
    bpy.ops.object.select_all(action = 'DESELECT')
    mesh = bpy.data.meshes.new(name='point cloud quad mesh')
    mesh.from_pydata(V,[],F)
    mesh.update()
    mesh.validate(verbose=True)
    P_mesh = bpy.data.objects.new('point cloud quad mesh object', mesh)
    P_mesh.location = location
    P_mesh.rotation_euler[0] = rotation[0] / 180. * np.pi
    P_mesh.rotation_euler[1] = rotation[1] / 180. * np.pi
    P_mesh.rotation_euler[2] = rotation[2] / 180. * np.pi
    P_mesh.scale = scale
    bpy.data.collections[0].objects.link(P_mesh)
    bpy.context.view_layer.update()

    # create geometry node for instancing
    P_mesh.modifiers.new("GeometryNode", type="NODES")
    MOD = P_mesh.modifiers[-1]
    name = "GeometryNodeTree"
    group = bpy.data.node_groups.new(name, "GeometryNodeTree")
    # group.inputs.new('NodeSocketGeometry', name)
    #### To add a new socket
    # Taken from here
    # https://blender.stackexchange.com/questions/305827/add-or-remove-item-socket-in-nodetree-node-group-new-items-tree-blende

    group.interface.new_socket(name='NodeSocketGeometry', in_out='INPUT', socket_type='NodeSocketGeometry', )
    group.interface.new_socket(name='NodeSocketGeometry', in_out='OUTPUT', socket_type='NodeSocketGeometry', )

    IN = group.nodes.new('NodeGroupInput')
    OUT = group.nodes.new('NodeGroupOutput')
    OUT.is_active_output = True
    IN.select = False
    OUT.select = False
    IN.location.x = -200 - IN.width
    OUT.location.x = 200

    # assign to MOD
    MOD.node_group = group

    NORMAL = group.nodes.new("GeometryNodeInputNormal")
    NORMAL.location.x = -800
    NORMAL.location.y = -200

    FA = group.nodes.new("GeometryNodeInputMeshFaceArea")
    FA.location.x = -800
    FA.location.y = -400

    # this is for versions before 3.4
    # TRANS = group.nodes.new("GeometryNodeAttributeTransfer")

    # this is for versions after 3.4
    SNS = group.nodes.new("GeometryNodeSampleNearestSurface")
    SNS.data_type = "FLOAT_VECTOR"
    SNS.location.x = -600
    SNS.location.y = -200
    
    # TRANS_AREA = group.nodes.new("GeometryNodeAttributeTransfer")
    # # TRANS_AREA.data_type = "FLOAT"
    # TRANS_AREA.location.x = -600
    # TRANS_AREA.location.y = -400

    SQRT = group.nodes.new("ShaderNodeMath")
    SQRT.operation = "SQRT"
    SQRT.location.x = -400
    SQRT.location.y = -400

    ALIGN = group.nodes.new("FunctionNodeAlignEulerToVector")
    ALIGN.axis = "Z"
    ALIGN.location.x = -400
    ALIGN.location.y = -200

    IN2PTS = group.nodes.new(type='GeometryNodeInstanceOnPoints')
    IN2PTS.location.x = 25
    IN2PTS.inputs["Scale"].default_value[0] =thickness
    IN2PTS.inputs["Scale"].default_value[1] = thickness
    IN2PTS.inputs["Scale"].default_value[2] = length

    MESH2PTS = group.nodes.new(type='GeometryNodeMeshToPoints')
    MESH2PTS.mode = 'FACES'
    MESH2PTS.location.x = -150

    OBJ = group.nodes.new("GeometryNodeObjectInfo")
    OBJ.inputs[0].default_value = arrow_obj
    # OBJ.transform_space = "RELATIVE"
    OBJ.location.x = -150
    OBJ.location.y = -200

    group.links.new(IN.outputs[0], MESH2PTS.inputs[0])
    group.links.new(IN.outputs[0], SNS.inputs[0])
    group.links.new(NORMAL.outputs[0], SNS.inputs[3])
    group.links.new(SNS.outputs[2], ALIGN.inputs[2])

    # ### group.links.new(IN.outputs[0], TRANS_AREA.inputs[0])
    # group.links.new(FA.outputs["Area"], TRANS_AREA.inputs["Attribute"])
    
    # group.links.new(TRANS_AREA.outputs[0], SQRT.inputs[0])
    # ### group.links.new(SQRT.outputs[0], IN2PTS.inputs[6])
    group.links.new(ALIGN.outputs[0], IN2PTS.inputs[5])
    group.links.new(MESH2PTS.outputs[0], IN2PTS.inputs[0])
    group.links.new(OBJ.outputs[3], IN2PTS.inputs[2])
    group.links.new(IN2PTS.outputs[0], OUT.inputs[0])


    return arrow_obj

