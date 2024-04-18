# -*- coding: utf-8 -*-
import bpy
import re

from mmd_tools_mod.mmd_tools.bpyutils import SceneOp
import mmd_tools_mod.mmd_tools.core.model as mmd_model

SORT_MODULE = None

try:
    from natsort import natsorted
    SORT_MODULE = 'natsort'
except ModuleNotFoundError as e:
    print('')
    print(f'mmd_tools_error: {e}')


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

        # sort
        sorted_joint_name_list = list(map(lambda x: x.mmd_joint.name_j, joint_objects))
        if SORT_MODULE == 'natsort':
            sorted_joint_name_list = natsorted(sorted_joint_name_list)
        else:
            sorted_joint_name_list = sorted(sorted_joint_name_list)

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


class MMDMOD_OT_joint_unique(bpy.types.Operator):
    bl_idname = 'mmd_tools_mod.joint_unique'
    bl_label  = 'rename duplicate joints to unique names'

    def execute(self, context):
        bpy.ops.ed.undo_push(message='mmd_tools_mod: before joint rename')

        joint_objects = list(filter(
            lambda x: hasattr(x, 'mmd_type') and x.mmd_type == 'JOINT',
            SceneOp(context).id_scene.objects
        ))

        joint_count = {}
        for joint in joint_objects:
            prefix = re.match(r'^([0-9]|[A-Z]){3}_', joint.name)

            if joint.mmd_joint.name_j in joint_count.keys():
                joint.name = joint.mmd_joint.name_j + '.{:0=3}'.format(joint_count[joint.mmd_joint.name_j])
                joint_count[joint.mmd_joint.name_j] += 1
            else:
                joint.name = joint.mmd_joint.name_j
                joint_count[joint.mmd_joint.name_j] = 1

            joint.mmd_joint.name_j = joint.name

            if prefix is not None:
                joint.name = prefix.group() + joint.name

        bpy.ops.ed.undo_push(message='mmd_tools_mod: before joint rename')

        return {'FINISHED'}

