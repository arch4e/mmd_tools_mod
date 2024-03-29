# -*- coding: utf-8 -*-
import bpy

from .common import BasePanel
from mmd_tools_mod.mmd_tools.bpyutils import SceneOp
import mmd_tools_mod.mmd_tools.core.model as mmd_model


class MMDMOD_JointUtility(BasePanel, bpy.types.Panel):
    bl_idname  = 'OBJECT_PT_mmd_tools_mod_joint_utility'
    bl_label   = 'Joints (Mod)'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        active_obj = context.active_object
        root = mmd_model.Model.findRoot(active_obj)
        if root is None:
            self.layout.label(text='Select a MMD Model')
            return

        col = self.layout.column()
        c = col.column(align=True)

        row = c.row()
        row.template_list(
            'MMD_TOOLS_UL_joints',
            '',
            SceneOp(context).id_scene, 'objects',
            root.mmd_root, 'active_joint_index',
        )
        tb = row.column()
        tb1 = tb.column(align=True)
        tb1.operator('mmd_tools.joint_add', text='', icon='ADD')
        tb1.operator('mmd_tools.joint_remove', text='', icon='REMOVE')
        tb1.menu('OBJECT_MT_mmd_tools_joint_menu', text='', icon='DOWNARROW_HLT')
        tb.separator()
        tb1 = tb.column(align=True)
        tb1.enabled = active_obj.mmd_type == 'JOINT'
        tb1.operator('mmd_tools.object_move', text='', icon='TRIA_UP').type = 'UP'
        tb1.operator('mmd_tools.object_move', text='', icon='TRIA_DOWN').type = 'DOWN'
        tb.separator()
        tb1 = tb.column(align=True)
        tb1.operator('mmd_tools_mod.joint_sort', text='', icon='CHECKMARK')

        col = c.column()
        row = col.row()
        row.operator('mmd_tools_mod.joint_add', text='Add Vertical Joint').JOINT_DIRECTION = 'VERTICAL'
        row.operator('mmd_tools_mod.joint_add', text='Add Horizontal Joint').JOINT_DIRECTION = 'HORIZONTAL'

