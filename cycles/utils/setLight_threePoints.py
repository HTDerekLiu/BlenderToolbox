import bpy

def setLight_threePoints(
    radius = 4, 
    height = 10, 
    intensity = 2000, 
    softness = 6):
    bpy.ops.object.light_add(type='POINT', radius=softness, location=(radius,0,height))
    KeyL = bpy.data.lights['Point']
    KeyL.energy = intensity
    bpy.ops.object.light_add(type='POINT', radius=softness, location=(0,radius,height))
    FillL = bpy.data.lights['Point.001']
    FillL.energy = intensity * 0.5
    bpy.ops.object.light_add(type='POINT', radius=softness, location=(0,-radius,height))
    RimL = bpy.data.lights['Point.002']
    RimL.energy = intensity * 0.2
    return [KeyL, FillL, RimL]