import bpy
import numpy as np

def readPLY(filePath, location, rotation_euler, scale):
	# example input types:
	# - location = (0.5, -0.5, 0)
	# - rotation_euler = (90, 0, 0)
	# - scale = (1,1,1)
	x = rotation_euler[0] * 1.0 / 180.0 * np.pi 
	y = rotation_euler[1] * 1.0 / 180.0 * np.pi 
	z = rotation_euler[2] * 1.0 / 180.0 * np.pi 
	angle = (x,y,z)
	bpy.ops.import_mesh.ply(filepath=filePath)
	mesh = bpy.data.objects[-1]
	mesh.location = location
	mesh.rotation_euler = angle
	mesh.scale = scale
	return mesh 