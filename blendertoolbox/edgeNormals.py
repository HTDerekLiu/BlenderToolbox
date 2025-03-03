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
import math

def edgeNormals(mesh, angle = 10):
    # this fix to handle blender > 4.1 is copied from 
    # https://blender.stackexchange.com/questions/316696/attributeerror-mesh-object-has-no-attribute-use-auto-smooth
    bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.shade_smooth()
    do_auto_smooth(bpy.context.object, angle)
    
def get_object_override(active_object, objects: list = None):

    if objects is None:
        objects = []
    else:
        objects = list(objects)

    if not active_object in objects:
        objects.append(active_object)

    assert all(isinstance(object, bpy.types.Object) for object in objects)

    return dict(
        selectable_objects = objects,
        selected_objects = objects,
        selected_editable_objects = objects,
        editable_objects = objects,
        visible_objects = objects,
        active_object = active_object,
        object = active_object,
    )


def has_smooth_by_angle(object: bpy.types.Object):
    for modifier in object.modifiers:

        if modifier.type != 'NODES':
            continue

        if modifier.node_group and 'Smooth by Angle' in modifier.node_group.name:
            return True

    return False


def do_auto_smooth(object: bpy.types.Object, angle = 30):
    try:
        object.data.use_auto_smooth=True
    except AttributeError:

        # may just use shade_smooth_by_angle but it modifies the mesh and goes against the new non-destructive auto-smooth idea

        if not hasattr(object, 'modifiers'):
            return

        if has_smooth_by_angle(object):
            return

        with bpy.context.temp_override(**get_object_override(object)):
            result = bpy.ops.object.modifier_add_node_group(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="geometry_nodes\\smooth_by_angle.blend\\NodeTree\\Smooth by Angle")
            if 'CANCELLED' in result:
                return

            modifier = object.modifiers[-1]
            modifier["Socket_1"] = True
            modifier["Input_1"] = math.radians(angle)
            object.update_tag()

