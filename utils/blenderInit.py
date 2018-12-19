import bpy

def blenderInit(resolution_x, resolution_y, numSamples = 128):
	# clear all
	bpy.ops.wm.read_homefile()
	bpy.ops.object.select_all(action = 'SELECT')
	bpy.ops.object.delete() 
	# use cycle
	bpy.context.scene.render.engine = 'CYCLES'
	bpy.context.scene.render.resolution_x = resolution_x # for faster preview
	bpy.context.scene.render.resolution_y = resolution_y # for faster preview
	bpy.context.scene.cycles.film_transparent = True
	bpy.context.scene.cycles.device = 'GPU'
	# bpy.context.scene.use_denoising = True
	bpy.context.scene.cycles.samples = numSamples # we can set much higher like 2000 samples for high quality images
	# bpy.context.scene.cycles.max_bounces = 7