# -*- coding: utf-8 -*-
import bpy
import re
from natsort import natsorted

from mmd_tools_mod.mmd_tools.bpyutils import SceneOp
import mmd_tools_mod.mmd_tools.core.model as mmd_model


class MMDMOD_OT_joint_add(bpy.types.Operator):
    bl_idname = 'mmd_tools_mod.joint_add'
    bl_label  = 'add joint'

    JOINT_DIRECTION: bpy.props.StringProperty()

    def execute(self, context):
        root = mmd_model.Model.findRoot(context.active_object)

        selected_objects = context.selected_objects
        for i in range(1, len(selected_objects)):
            # skip when target object is not rigid body(mesh)
            if selected_objects[i - 1].type != 'MESH' or selected_objects[i].type != 'MESH':
                continue

            # select rigid body pair
            bpy.ops.object.select_all(action='DESELECT')
            selected_objects[i - 1].select = True
            selected_objects[i].select = True

            # create joint
            bpy.ops.mmd_tools.joint_add()
            _joint_index = root.mmd_root.active_joint_index
            _joint = SceneOp(context).id_scene.objects[_joint_index]

            # rename joint
            if self.JOINT_DIRECTION == 'VERTICAL':
                context.active_object.mmd_joint.name_j =  _joint.name + '_V'
                _joint.name = 'ZZZ_' + context.active_object.mmd_joint.name_j # 'ZZZ_' is order prefix
            else:
                context.active_object.mmd_joint.name_j =  _joint.name + '_H'
                _joint.name = 'ZZZ_' + context.active_object.mmd_joint.name_j # 'ZZZ_' is order prefix

        return {'FINISHED'}


class MMDMOD_OT_joint_sort(bpy.types.Operator):
    bl_idname = 'mmd_tools_mod.joint_sort'
    bl_label  = 'sort joints (joints with duplicate names will not be modified)'

    def execute(self, context):
        # init
        bpy.ops.ed.undo_push(message='mmd_tools_mod: before joint sort')
        joint_objects = list(filter(
            lambda x: hasattr(x, 'mmd_type') and x.mmd_type == 'JOINT',
            SceneOp(context).id_scene.objects
        ))
        sorted_joint_name_list = natsorted(list(map(lambda x: x.mmd_joint.name_j, joint_objects)))

        # create joint dict
        joint_dict = {}
        for _joint in joint_objects:
            joint_dict[_joint.mmd_joint.name_j] = _joint

        # sort the list in ascending order sequentially from the beginning
        # note: the order of joints is determined by the prefix of the object name
        for i in range(len(sorted_joint_name_list)):
            joint = joint_dict[sorted_joint_name_list[i]]

            if re.match(r'^([0-9]|[A-Z]){3}_', joint.name):
                joint.name = joint.name[4:] # '4' is prefix length

            joint.name = '{:0=3}_{}'.format(i, joint.name)

        bpy.ops.ed.undo_push(message='mmd_tools_mod: after joint sort')

        return {'FINISHED'}

