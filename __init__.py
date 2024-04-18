# -*- coding: utf-8 -*-
import bpy

from .operator.joint import MMDMOD_OT_joint_add, MMDMOD_OT_joint_sort, MMDMOD_OT_joint_unique
from .ui.ex_rigidbody_menu import MMDMOD_JointUtility


bl_info = {
    'name'    : 'mmd_tools_mod',
    'category': '3D View',
    'location': '',
    'version' : (4,0,0),
    'blender' : (3,0,0),
    'author'  : 'arch4e'
}


# Menus and Panels are displayed in the order of registration,
# so they are not arranged alphabetically.
classes = [
    MMDMOD_OT_joint_add,
    MMDMOD_OT_joint_sort,
    MMDMOD_OT_joint_unique,
    MMDMOD_JointUtility,
]


def register():
    # Operator
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    # Operator
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    unregister()
    register()

