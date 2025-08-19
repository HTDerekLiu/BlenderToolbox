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

def blenderInit(
        resolution_x: int, 
        resolution_y: int, 
        numSamples: int = 128, 
        exposure: float = 1.5, 
        use_gpu: bool = True,
        ):
    # clear all
    bpy.ops.wm.read_homefile()
    bpy.ops.object.select_all(action = 'SELECT')
    bpy.ops.object.delete() 
    # use cycle
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.resolution_x = resolution_x 
    bpy.context.scene.render.resolution_y = resolution_y 
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.cycles.samples = numSamples 
    bpy.context.scene.cycles.max_bounces = 6
    bpy.context.scene.cycles.film_exposure = exposure
    bpy.context.scene.render.resolution_percentage = 100

    # Denoising
    # Note: currently I stop denoising as it will also denoise the alpha shadow channel. TODO: implement blurring shadow in the composite node
    bpy.data.scenes[0].view_layers[0]['cycles']['use_denoising'] = 0
    # bpy.data.scenes[0].view_layers[0]['cycles']['use_denoising'] = 1

    # set devices
    # cyclePref.compute_device_type = 'CUDA'
    if use_gpu:
        bpy.context.preferences.addons['cycles'].preferences.refresh_devices()
        num_devices = len(bpy.context.preferences.addons['cycles'].preferences.devices)
        if num_devices == 0:
            print("WARNING: you are not using GPU for rendering")
        for device in bpy.context.preferences.addons['cycles'].preferences.devices:
            if device.type != 'CPU':
                print("using device: ", device)
                device.use = True
                bpy.context.preferences.addons['cycles'].preferences.compute_device_type = device.type
        bpy.context.scene.cycles.device = 'GPU'
    return 0