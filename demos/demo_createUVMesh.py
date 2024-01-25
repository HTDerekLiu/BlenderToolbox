import sys, os
sys.path.append(os.path.join(os.path.abspath(os.getcwd()),'..')) # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
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
bpy.ops.export_scene.obj(filepath='./test.obj', check_existing=True, filter_glob='*.obj;*.mtl', use_selection=False, use_animation=False, use_mesh_modifiers=True, use_edges=False, use_smooth_groups=False, use_smooth_groups_bitflags=False, use_normals=False, use_uvs=True, use_materials=False, use_triangles=False, use_nurbs=False, use_vertex_groups=False, use_blen_objects=True, group_by_object=False, group_by_material=False, keep_vertex_order=False, global_scale=1.0, path_mode='AUTO', axis_forward='Y', axis_up='Z')

