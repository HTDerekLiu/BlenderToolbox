import bpy 

def subdivision(mesh, level = 0):
	bpy.context.scene.objects.active = mesh
	bpy.ops.object.modifier_add(type='SUBSURF')
	mesh.modifiers["Subsurf"].render_levels = level # rendering subdivision level
	mesh.modifiers["Subsurf"].levels = 0 # subdivision level in 3D view