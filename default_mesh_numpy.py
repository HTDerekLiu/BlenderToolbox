import blendertoolbox as bt
import numpy as np

'''
RENDER A MESH STEP-BY-STEP:
1. run "python default_mesh_numpy.py" in terminal, then terminate the code when it starts rendering. This step outputs a "test.blend"
2. open "test.blend" with your blender software
3. in blender UI, adjust:
    - "mesh_location", "mesh_rotation", "mesh_scale" of the mesh
4. type in the adjusted mesh parameters from UI to "default_mesh_numpy.py"
5. run "python default_mesh_numpy.py" again (wait a couple minutes) to output your final image
'''

V = np.array([[1,1,1],[-1,1,-1],[-1,-1,1],[1,-1,-1]], dtype=np.float32) # vertex list
F = np.array([[0,1,2],[0,2,3],[0,3,1],[2,1,3]], dtype=np.int32) # face list

arguments = {
  "output_path": "./default_mesh_numpy.png",
  "image_resolution": [720, 720], # recommend >1080 for paper figures
  "number_of_samples": 200, # recommend >200 for paper figures
  "vertices": V,
  "faces": F,
  "mesh_position": (0,0,0.67) , # UI: click mesh > Transform > Location
  "mesh_rotation": (0,0,0) , # UI: click mesh > Transform > Rotation
  "mesh_scale": (.5,.5,.5), # UI: click mesh > Transform > Scale
  "shading": "smooth", # either "flat" or "smooth"
  "subdivision_iteration": 0, # integer
  "mesh_RGB": [144.0/255, 210.0/255, 236.0/255], # mesh RGB
  "light_angle": (6, -30, -155) # UI: click Sun > Transform > Rotation
}
bt.render_mesh_default(arguments)
