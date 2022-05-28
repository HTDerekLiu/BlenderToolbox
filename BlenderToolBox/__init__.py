from . blenderInit import blenderInit
from . colorMap import colorMap
from . copyToVertexSubset import copyToVertexSubset
from . copyArrowToVertex import copyArrowToVertex
from . colorObj import colorObj
from . createArrow import createArrow
from . drawPoints import drawPoints
from . drawLines import drawLines
from . drawEdgeSubset import drawEdgeSubset
from . drawBoundaryLoop import drawBoundaryLoop
from . drawSphere import drawSphere
from . discreteColor import discreteColor
from . edgeNormals import edgeNormals
from . getEdgeWire import getEdgeWire
from . invisibleGround import invisibleGround
from . initColorNode import initColorNode
from . lookAt import lookAt
from . loadShader import loadShader
from . readImagePlane import readImagePlane
from . readMesh import readMesh
from . readNumpyMesh import readNumpyMesh
from . readOBJ import readOBJ
from . readPLY import readPLY
from . renderImage import renderImage
from . renderAnimation import renderAnimation
from . render_mesh_default import render_mesh_default
from . recalculateNormals import recalculateNormals
from . selectOBJ import selectOBJ
from . setCamera import setCamera
from .setCamera_from_UI import setCamera_from_UI
from . setCamera_orthographic import setCamera_orthographic
from . setCameraPath import setCameraPath
from . setLight_sun import setLight_sun
from . setLight_ambient import setLight_ambient
from . setLight_threePoints import setLight_threePoints
from . setMat_amber import setMat_amber
from . setMat_balloon import setMat_balloon
from . setMat_carPaint import setMat_carPaint
from . setMat_chrome import setMat_chrome
from . setMat_crackedCeramic import setMat_crackedCeramic
from . setMat_ceramic import setMat_ceramic
from . setMat_edge import setMat_edge
from . setMat_emission import setMat_emission
from . setMat_glass import setMat_glass
from . setMat_honey import setMat_honey
from . setMat_singleColor import setMat_singleColor
from . setMat_stone import setMat_stone
from . setMat_transparent import setMat_transparent
from . setMat_transparentWithEdge import setMat_transparentWithEdge
from . setMat_texture import setMat_texture
from . setMat_pointCloud import setMat_pointCloud
from . setMat_poop import setMat_poop
from . setMat_plastic import setMat_plastic
from . setMat_VColor import setMat_VColor
from . setMat_VColorAO import setMat_VColorAO
from . setMat_VColorEdge import setMat_VColorEdge
from . setMat_monotone import setMat_monotone
from . setMat_matcap import setMat_matcap
from . setMat_muscle import setMat_muscle
from . setMat_metal import setMat_metal
from . subdivision import subdivision
from . shadowThreshold import shadowThreshold

derekBlue = (144.0/255, 210.0/255, 236.0/255, 1)
coralRed = (250.0/255, 114.0/255, 104.0/255, 1)
iglGreen = (153.0/255, 203.0/255, 67.0/255, 1)
caltechOrange = (255.0/255, 108.0/255, 12.0/255, 1)
royalBlue = (0/255, 35/255, 102/255, 1)
royalYellow = (250.0/255,218.0/255,94.0/255, 1)
white = (1,1,1,1)
black = (0,0,0,1)

# color palette for color blindness (source: http://mkweb.bcgsc.ca/colorblind)
cb_black = (0/255.0, 0/255.0, 236/255.0, 1)
cb_orange = (230/255.0, 159/255.0, 0/255.0, 1)
cb_skyBlue = (86/255.0, 180/255.0, 233/255.0, 1)
cb_green = (0/255.0, 158/255.0, 115/255.0, 1)
cb_yellow = (240/255.0, 228/255.0, 66/255.0, 1)
cb_blue = (0/255.0, 114/255.0, 178/255.0, 1)
cb_vermillion = (213/255.0, 94/255.0, 0/255.0, 1)
cb_purple = (204/255.0, 121/255.0, 167/255.0, 1)
