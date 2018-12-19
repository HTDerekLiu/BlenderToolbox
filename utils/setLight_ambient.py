import bpy

def setLight_ambient(color = (0,0,0)):
	bpy.data.scenes[0].world.horizon_color = color