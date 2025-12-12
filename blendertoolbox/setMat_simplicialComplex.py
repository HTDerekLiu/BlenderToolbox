# Copyright 2025 Hsueh-Ti Derek Liu
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
import numpy as np

from .setMat_singleColor import setMat_singleColor
from .setMat_graph import setMat_graph

def setMat_simplicialComplex(
    meshFace, meshCurveNetwork,
    nodeSize  , edgeThickness,
    nodeColor , edgeColor, faceColor,
    edge_resolution=8):
    """
    This function sets the material for a simplicial complex.

    Inputs:
    meshFace: blender mesh object for the face
    meshCurveNetwork: blender mesh object for the curve network
    nodeSize: size of the nodes
    edgeThickness: thickness of the edges
    nodeColor: color object of the nodes
    edgeColor: color object of the edges
    faceColor: color object of the face
    edge_resolution: resolution of the edges for smoothness

    Outputs:
    None
    """
    setMat_singleColor(meshFace, faceColor, 0.0)
    setMat_graph(meshCurveNetwork, nodeSize,  edgeThickness, nodeColor, edgeColor, edge_resolution)