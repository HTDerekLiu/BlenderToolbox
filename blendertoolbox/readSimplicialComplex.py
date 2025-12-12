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

from .readNumpyMesh import readNumpyMesh
from .setGraphMesh import setGraphMesh

def readSimplicialComplex(V,E,F,location,rotation,scale):
    """
    This function reads a simplicial complex from numpy arrays and returns the mesh face and curve network.

    Inputs:
    V: numpy array of vertex locations
    E: numpy array of edge indices
    F: numpy array of face indices
    location: tuple of location
    rotation: tuple of rotation
    scale: tuple of scale

    Outputs:
    meshFace: blender mesh object for the face
    meshCurveNetwork: blender mesh object for the curve network
    """
    meshFace = readNumpyMesh(V, F, location, rotation, scale)
    meshCurveNetwork = setGraphMesh(V, E, location, rotation, scale)
    return meshFace, meshCurveNetwork