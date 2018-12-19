import bpy

def invisibleGround(location = (0,0,0), radius = 5):
	# initialize a ground for shadow
	bpy.context.scene.cycles.film_transparent = True
	bpy.ops.mesh.primitive_plane_add(location = location, radius = radius)
	bpy.context.object.cycles.is_shadow_catcher = True