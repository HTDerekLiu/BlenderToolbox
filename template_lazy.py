import sys, os
sys.path.append(os.path.join(os.path.abspath(os.getcwd()))) # change this to your path to “path/to/BlenderToolbox/
import blendertoolbox as bt

'''
RENDER A MESH STEP-BY-STEP:
1. copy "template_lazy.py" to your preferred local folder
2. In "template_lazy.py":
    - change "mesh_path" to your desired mesh path
    - change to sys.path.append('path/to/BlenderToolBox/cycles/')
3. run "blender --background --python template_lazy.py" in terminal, then terminate the code when it starts rendering. This step outputs a "test.blend"
4. open "test.blend" with your blender software
5. in blender UI, adjust:
    - "mesh_location", "mesh_rotation", "mesh_scale" of the mesh
6. type in the adjusted mesh parameters from UI to "template_lazy.py"
7. run "blender --background --python template_lazy.py" again (wait a couple minutes) to output your final image
'''

arguments = {
  "output_path": "./template_lazy.png",
  "image_resolution": [720, 720], # recommend >1080 for paper figures
  "number_of_samples": 200, # recommend >200 for paper figures
  "mesh_path": "./meshes/spot.ply", # either .ply or .obj
  "mesh_position": (1.12, -0.14, 0), # UI: click mesh > Transform > Location
  "mesh_rotation": (90, 0, 227), # UI: click mesh > Transform > Rotation
  "mesh_scale": (1.5,1.5,1.5), # UI: click mesh > Transform > Scale
  "shading": "smooth", # either "flat" or "smooth"
  "subdivision_iteration": 0, # integer
  "mesh_RGB": [144.0/255, 210.0/255, 236.0/255], # mesh RGB
  "light_angle": (6, -30, -155) # UI: click Sun > Transform > Rotation
}
bt.render_mesh_default(arguments)