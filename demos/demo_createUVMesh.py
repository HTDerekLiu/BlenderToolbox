import sys, os
sys.path.append(os.path.join(os.path.abspath(os.getcwd()),'..')) # change this to your path to “path/to/BlenderToolbox/
import blendertoolbox as bt
import bpy, bmesh
import numpy as np
cwd = os.getcwd()

## initialize blender
imgRes_x = 480 
imgRes_y = 480 
numSamples = 100 
exposure = 2.0
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read mesh (choose either readPLY or readOBJ)
meshPath = '../meshes/spot.ply'
location = (0,0,0) # (UI: click mesh > Transform > Location)
rotation = (0,0,0) # (UI: click mesh > Transform > Rotation)
scale = (1,1,1) # (UI: click mesh > Transform > Scale)
mesh = bt.readMesh(meshPath, location, rotation, scale)

## use blender built-in smart UV unwrap
bpy.ops.object.editmode_toggle() # enter edit mode
bpy.ops.uv.smart_project()
bpy.ops.object.editmode_toggle() # enter object mode

## export obj
bpy.ops.wm.obj_export(filepath='./test.obj', check_existing=True, filter_glob='*.obj;*.mtl', export_selected_objects=False,
                      export_animation=False, apply_modifiers=True,   export_smooth_groups=False,
                      export_normals=False, export_uv=True, export_materials=False,
                      export_triangulated_mesh=False, export_curves_as_nurbs=False, export_vertex_groups=False,
                      export_object_groups=False, export_material_groups=False,  global_scale=1.0,
                      path_mode='AUTO', forward_axis='Y', up_axis='Z')

