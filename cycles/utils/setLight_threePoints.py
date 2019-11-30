import bpy

def setLight_threePoints(dist, height, intensity, softness):
    bpy.ops.object.light_add(type='POINT', radius=softness, location=(dist,0,height))
    KeyL = bpy.data.lights['Point']
    KeyL.energy = intensity
    bpy.ops.object.light_add(type='POINT', radius=softness, location=(0,dist,height))
    FillL = bpy.data.lights['Point.001']
    FillL.energy = intensity * 0.5
    bpy.ops.object.light_add(type='POINT', radius=softness, location=(0,-dist,height))
    RimL = bpy.data.lights['Point.002']
    RimL.energy = intensity * 0.2
    return [KeyL, FillL, RimL]