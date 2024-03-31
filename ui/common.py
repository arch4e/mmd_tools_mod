# -*- coding: utf-8 -*-
from mmd_tools_mod.mmd_tools import bpyutils


class BasePanel(object):
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category    = 'MMD'

    # sync _PanelBase in UuuNyaa/blender_mmd_tools
    @classmethod
    def poll(cls, _context):
        return bpyutils.addon_preferences('enable_mmd_model_production_features', True)

