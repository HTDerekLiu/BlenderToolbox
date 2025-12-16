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
from . initColorNode import initColorNode

def setMat_thindielectric(mesh, meshColor, eta=1.5, roughness=0.0):
    """
    Creates a thin dielectric material mimicking Mitsuba's thindielectric BSDF.
    
    Thin dielectric represents a thin, transparent surface like soap bubbles,
    thin glass, or plastic film where:
    - Light passes through without volumetric absorption
    - Fresnel-based specular reflection at grazing angles
    - Specular transmission at normal incidence
    
    Parameters:
    -----------
    mesh : bpy.types.Object
        The mesh object to apply the material to
    meshColor : colorObj
        Color object with RGBA, H, S, V, Bright, Contrast values
    eta : float
        Index of refraction (default: 1.5 for glass)
        Common values: 1.33 (water), 1.5 (glass), 1.49 (plastic)
    roughness : float
        Surface roughness (0.0 = perfectly smooth/specular, 1.0 = rough)
        For true thin dielectric behavior, keep this low (default: 0.0)
    """
    mat = bpy.data.materials.new('ThinDielectricMaterial')
    mesh.data.materials.append(mat)
    mesh.active_material = mat
    mat.use_nodes = True
    tree = mat.node_tree
    
    # Clear default nodes
    for node in tree.nodes:
        tree.nodes.remove(node)
    
    # Create output node
    output = tree.nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    # Create Fresnel node for IOR-based mixing
    fresnel = tree.nodes.new('ShaderNodeFresnel')
    fresnel.inputs['IOR'].default_value = eta
    fresnel.location = (-200, 100)
    
    # Create Glossy BSDF for specular reflection
    glossy = tree.nodes.new('ShaderNodeBsdfGlossy')
    glossy.inputs['Roughness'].default_value = roughness
    glossy.location = (-200, -100)
    
    # Create Transparent BSDF for thin transmission (no refraction offset)
    # This is key for thin dielectric - light passes through without volumetric effects
    transparent = tree.nodes.new('ShaderNodeBsdfTransparent')
    transparent.location = (-200, -250)
    
    # Create color nodes for tinting
    # HSV node for color adjustment
    hsv = tree.nodes.new('ShaderNodeHueSaturation')
    hsv.inputs['Color'].default_value = meshColor.RGBA
    hsv.inputs['Saturation'].default_value = meshColor.S
    hsv.inputs['Value'].default_value = meshColor.V
    hsv.inputs['Hue'].default_value = meshColor.H
    hsv.location = (-600, -100)
    
    # Brightness/Contrast node
    bc = tree.nodes.new('ShaderNodeBrightContrast')
    bc.inputs['Bright'].default_value = meshColor.B
    bc.inputs['Contrast'].default_value = meshColor.C
    bc.location = (-400, -100)
    
    # Link color nodes
    tree.links.new(hsv.outputs['Color'], bc.inputs['Color'])
    tree.links.new(bc.outputs['Color'], glossy.inputs['Color'])
    tree.links.new(bc.outputs['Color'], transparent.inputs['Color'])
    
    # Create Mix Shader to blend reflection and transmission based on Fresnel
    mix = tree.nodes.new('ShaderNodeMixShader')
    mix.location = (200, 0)
    
    # Connect: Fresnel controls mix (0 = transmission, 1 = reflection)
    tree.links.new(fresnel.outputs['Fac'], mix.inputs['Fac'])
    tree.links.new(transparent.outputs['BSDF'], mix.inputs[1])  # First shader (transmission)
    tree.links.new(glossy.outputs['BSDF'], mix.inputs[2])       # Second shader (reflection)
    
    # Connect to output
    tree.links.new(mix.outputs['Shader'], output.inputs['Surface'])
    
    return mat

