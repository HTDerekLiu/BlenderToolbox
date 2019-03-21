import bpy

def setMat_pointCloud(mesh, \
                ptColor, \
                ptSize, \
                ptSaturation = 1.0, \
                ptBrightness = 1.0): 
    # initialize a primitive sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius = 1.0, location = (1e7,1e7,1e7))
    sphere = bpy.context.object
    bpy.ops.object.shade_smooth()
    mat = bpy.data.materials.new(name="sphereMat")
    sphere.data.materials.append(mat)
    sphere.active_material = mat
    mat.use_nodes = True
    tree = mat.node_tree
    tree.nodes.new('ShaderNodeHueSaturation')
    tree.nodes["Hue Saturation Value"].inputs['Color'].default_value = ptColor
    tree.nodes["Hue Saturation Value"].inputs['Saturation'].default_value = ptSaturation
    tree.nodes["Hue Saturation Value"].inputs['Value'].default_value = ptBrightness
    tree.links.new(tree.nodes["Hue Saturation Value"].outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])

    # init particle system
    bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.particle_system_add()
    bpy.data.particles["ParticleSettings"].count = len(mesh.data.vertices)
    bpy.data.particles["ParticleSettings"].frame_start = 0
    bpy.data.particles["ParticleSettings"].frame_end = 0
    bpy.data.particles["ParticleSettings"].render_type = 'OBJECT'
    bpy.data.particles["ParticleSettings"].instance_object = sphere
    bpy.data.particles["ParticleSettings"].emit_from = 'VERT'
    bpy.data.particles["ParticleSettings"].particle_size = ptSize
    bpy.data.particles["ParticleSettings"].physics_type = 'NO'
    bpy.data.particles["ParticleSettings"].use_emit_random = False
