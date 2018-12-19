import bpy

def drawPointCloud(mesh, ptColor, ptSize, numPt, emitFrom = 'VERT', ptSaturation = 1.0, ptBrightness = 1.0): 
    # initialize a primitive sphere
    bpy.ops.mesh.primitive_uv_sphere_add(size = 1.0, location = (1000,1000,1000))
    sphere = bpy.context.object
    bpy.ops.object.shade_smooth()
    mat = bpy.data.materials.new(name="sphereMat")
    sphere.data.materials.append(mat)
    mat.use_nodes = True
    tree = mat.node_tree
    tree.nodes.new('ShaderNodeHueSaturation')
    tree.links.new(tree.nodes["Hue Saturation Value"].outputs['Color'], tree.nodes['Diffuse BSDF'].inputs['Color'])
    tree.nodes["Hue Saturation Value"].inputs['Color'].default_value = ptColor
    tree.nodes["Hue Saturation Value"].inputs['Saturation'].default_value = ptSaturation
    tree.nodes["Hue Saturation Value"].inputs['Value'].default_value = ptBrightness

    # init particle system
    bpy.context.scene.objects.active = mesh
    bpy.ops.object.particle_system_add()
    bpy.data.particles["ParticleSettings"].count = numPt
    bpy.data.particles["ParticleSettings"].frame_start = 0
    bpy.data.particles["ParticleSettings"].frame_end = 0
    bpy.data.particles["ParticleSettings"].render_type = 'OBJECT'
    bpy.data.particles["ParticleSettings"].dupli_object = sphere
    bpy.data.particles["ParticleSettings"].emit_from = emitFrom # place points on either 'VERT' or 'FACE'
    bpy.data.particles["ParticleSettings"].particle_size = ptSize
    bpy.data.particles["ParticleSettings"].physics_type = 'NO'
    bpy.data.particles["ParticleSettings"].use_render_emitter = False
