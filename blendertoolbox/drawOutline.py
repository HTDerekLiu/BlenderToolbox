# Copyright 2024 Oded Stein
import bpy

def drawOutline(thickness = 1.0, alpha = 0.85):
    bpy.data.scenes["Scene"].render.use_freestyle = True
    bpy.data.scenes["Scene"].render.line_thickness_mode = "RELATIVE"
    freestyle_settings = bpy.context.window.view_layer.freestyle_settings
    lineset = freestyle_settings.linesets.active
    lineset.select_silhouette = False
    lineset.select_crease = False
    lineset.select_border = False
    lineset.select_contour = True
    bpy.data.linestyles["LineStyle"].alpha = alpha
    bpy.data.linestyles["LineStyle"].thickness = thickness