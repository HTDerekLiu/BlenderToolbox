import bpy

def setGraphMaterial(obj, node_size,  edge_thickness, node_color, edge_color, edge_resolution = 8):
    # =============================================================================
    # Add Geometry Nodes for edge thickness and node spheres
    # =============================================================================
    geo_mod = obj.modifiers.new(name="GraphViz", type='NODES')

    # Create geometry node tree
    node_group = bpy.data.node_groups.new("GraphVisualization", 'GeometryNodeTree')
    geo_mod.node_group = node_group

    nodes = node_group.nodes
    links = node_group.links

    # Create interface sockets
    node_group.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    node_group.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')

    # Add input/output nodes
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-600, 0)
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (600, 0)

    # --- EDGES: Mesh to Curve -> Curve to Mesh with circle profile ---
    mesh_to_curve = nodes.new('GeometryNodeMeshToCurve')
    mesh_to_curve.location = (-400, 100)

    curve_circle = nodes.new('GeometryNodeCurvePrimitiveCircle')
    curve_circle.location = (-200, -100)
    curve_circle.inputs['Resolution'].default_value = edge_resolution
    curve_circle.inputs['Radius'].default_value = edge_thickness

    curve_to_mesh = nodes.new('GeometryNodeCurveToMesh')
    curve_to_mesh.location = (0, 100)

    # --- NODES: Instance spheres at original vertex positions ---
    # We need the original mesh points, so capture them before curve conversion
    mesh_to_points = nodes.new('GeometryNodeMeshToPoints')
    mesh_to_points.location = (-400, -200)

    uv_sphere = nodes.new('GeometryNodeMeshUVSphere')
    uv_sphere.location = (-200, -300)
    uv_sphere.inputs['Segments'].default_value = 16
    uv_sphere.inputs['Rings'].default_value = 8
    uv_sphere.inputs['Radius'].default_value = node_size

    instance_on_points = nodes.new('GeometryNodeInstanceOnPoints')
    instance_on_points.location = (0, -200)

    realize_instances = nodes.new('GeometryNodeRealizeInstances')
    realize_instances.location = (200, -200)

    # --- Combine edges and nodes ---
    join_geometry = nodes.new('GeometryNodeJoinGeometry')
    join_geometry.location = (400, 0)

    # Connect nodes
    links.new(input_node.outputs[0], mesh_to_curve.inputs['Mesh'])
    links.new(input_node.outputs[0], mesh_to_points.inputs['Mesh'])
    links.new(mesh_to_curve.outputs['Curve'], curve_to_mesh.inputs['Curve'])
    links.new(curve_circle.outputs['Curve'], curve_to_mesh.inputs['Profile Curve'])
    links.new(mesh_to_points.outputs['Points'], instance_on_points.inputs['Points'])
    links.new(uv_sphere.outputs['Mesh'], instance_on_points.inputs['Instance'])
    links.new(instance_on_points.outputs['Instances'], realize_instances.inputs['Geometry'])
    links.new(curve_to_mesh.outputs['Mesh'], join_geometry.inputs['Geometry'])
    links.new(realize_instances.outputs['Geometry'], join_geometry.inputs['Geometry'])
    links.new(join_geometry.outputs['Geometry'], output_node.inputs[0])

    # Edge material with full color control
    edge_mat = create_material_from_colorObj("EdgeMaterial", edge_color, roughness=0.5)

    # Node material with full color control
    node_mat = create_material_from_colorObj("NodeMaterial", node_color, roughness=0.3)

    # Assign materials to object
    obj.data.materials.append(edge_mat)  # Index 0
    obj.data.materials.append(node_mat)  # Index 1

    # --- Add Set Material nodes in geometry nodes to assign materials ---
    set_mat_edges = nodes.new('GeometryNodeSetMaterial')
    set_mat_edges.location = (200, 100)
    set_mat_edges.inputs['Material'].default_value = edge_mat

    set_mat_nodes = nodes.new('GeometryNodeSetMaterial')
    set_mat_nodes.location = (300, -200)
    set_mat_nodes.inputs['Material'].default_value = node_mat

    # Re-wire with materials
    links.new(curve_to_mesh.outputs['Mesh'], set_mat_edges.inputs['Geometry'])
    links.new(realize_instances.outputs['Geometry'], set_mat_nodes.inputs['Geometry'])

    # Clear old join connections and reconnect
    for link in list(links):
        if link.to_node == join_geometry:
            links.remove(link)

    links.new(set_mat_edges.outputs['Geometry'], join_geometry.inputs['Geometry'])
    links.new(set_mat_nodes.outputs['Geometry'], join_geometry.inputs['Geometry'])
    
def create_material_from_colorObj(name, colorObj, roughness=0.5):
    
    """
    Create a material with HSV and Brightness/Contrast control from colorObj.
    This matches the style used in BlenderToolbox's setMat functions.
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    tree = mat.node_tree
    
    # Get the Principled BSDF node
    bsdf = tree.nodes["Principled BSDF"]
    bsdf.inputs['Roughness'].default_value = roughness
    
    # Create HSV node (Hue/Saturation/Value)
    hsv_node = tree.nodes.new('ShaderNodeHueSaturation')
    hsv_node.inputs['Color'].default_value = colorObj.RGBA
    hsv_node.inputs['Hue'].default_value = colorObj.H
    hsv_node.inputs['Saturation'].default_value = colorObj.S
    hsv_node.inputs['Value'].default_value = colorObj.V
    hsv_node.location = (-400, 300)
    
    # Create Brightness/Contrast node
    bc_node = tree.nodes.new('ShaderNodeBrightContrast')
    bc_node.inputs['Bright'].default_value = colorObj.B
    bc_node.inputs['Contrast'].default_value = colorObj.C
    bc_node.location = (-200, 300)
    
    # Connect: HSV -> Brightness/Contrast -> Principled BSDF
    tree.links.new(hsv_node.outputs['Color'], bc_node.inputs['Color'])
    tree.links.new(bc_node.outputs['Color'], bsdf.inputs['Base Color'])
    
    return mat