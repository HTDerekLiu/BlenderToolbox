# Copyright 2020 Hsueh-Ti Derek Liu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import bpy

def blenderInit(resolution_x, resolution_y, numSamples = 128, exposure = 1.5, use_GPU = True):
	# clear all
	bpy.ops.wm.read_homefile()
	bpy.ops.object.select_all(action = 'SELECT')
	bpy.ops.object.delete() 
	# use cycle
	bpy.context.scene.render.engine = 'CYCLES'
	bpy.context.scene.render.resolution_x = resolution_x 
	bpy.context.scene.render.resolution_y = resolution_y 
	# bpy.context.scene.cycles.film_transparent = True
	bpy.context.scene.render.film_transparent = True
	bpy.context.scene.cycles.samples = numSamples 
	bpy.context.scene.cycles.max_bounces = 6
	bpy.context.scene.cycles.film_exposure = exposure

	# Denoising
	# Note: currently I stop denoising as it will also denoise the alpha shadow channel. TODO: implement blurring shadow in the composite node
	bpy.data.scenes[0].view_layers[0]['cycles']['use_denoising'] = 0
	# bpy.data.scenes[0].view_layers[0]['cycles']['use_denoising'] = 1

	# set devices
	cyclePref  = bpy.context.preferences.addons['cycles'].preferences
	for dev in cyclePref.devices:
		print("using rendering device", dev.name, ":", dev.use)
	if use_GPU:
		bpy.context.scene.cycles.device = "GPU"
	else:
		bpy.context.scene.cycles.device = "CPU"
	print("cycles rendering with:", bpy.context.scene.cycles.device)
	return 0

# RIP
# try:
# 	cyclePref.compute_device_type = 'CUDA'
# except:
# 	print("========================================")
# 	print("You are using CPU rendering. Please see the [Notes] section on the GitHub if you want to switch to GPU rendering.")
# 	print("========================================")
# for dev in cyclePref.devices:
# 	if dev.type == "CPU" and useBothCPUGPU is False:
# 		dev.use = False
# 	else:
# 		dev.use = True