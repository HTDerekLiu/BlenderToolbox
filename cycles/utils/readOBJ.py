import bpy
import numpy as np

def readOBJ(filePath, location, rotation_euler, scale):
	x = rotation_euler[0] * 1.0 / 180.0 * np.pi 
	y = rotation_euler[1] * 1.0 / 180.0 * np.pi 
	z = rotation_euler[2] * 1.0 / 180.0 * np.pi 
	angle = (x,y,z)
	bpy.ops.import_scene.obj(filepath=filePath)
	mesh = bpy.data.objects[-1]
	mesh.name = 'Mesh'
	mesh.location = location
	mesh.rotation_euler = angle
	mesh.scale = scale
	return mesh 