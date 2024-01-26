import blendertoolbox as bt

'''
RENDER A MESH STEP-BY-STEP:
1. run "python default_point_cloud.py" in terminal, then terminate the code when it starts rendering. This step outputs a "test.blend"
2. open "test.blend" with your blender software
3. in blender UI, adjust:
    - "mesh_location", "mesh_rotation", "mesh_scale" of the mesh
4. type in the adjusted mesh parameters from UI to "default_point_cloud.py"
5. run "python default_point_cloud.py" again (wait a couple minutes) to output your final image
'''

arguments = {
  "output_path": "./default_point_cloud.png",
  "image_resolution": [720, 720], # recommend >1080 for paper figures
  "number_of_samples": 200, # recommend >200 for paper figures
  "mesh_path": "./meshes/spot.ply", # either .ply or .obj
  "mesh_position": (1.12, -0.14, 0), # UI: click mesh > Transform > Location
  "mesh_rotation": (90, 0, 227), # UI: click mesh > Transform > Rotation
  "mesh_scale": (1.5,1.5,1.5), # UI: click mesh > Transform > Scale
  "mesh_RGB": [144.0/255, 210.0/255, 236.0/255], # mesh RGB
  "light_angle": (6, -30, -155) # UI: click Sun > Transform > Rotation
}
bt.render_point_cloud_default(arguments)