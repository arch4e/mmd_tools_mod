# -*- coding: utf-8 -*-
import bpy

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
                _joint.name = context.active_object.mmd_joint.name_j = '縦_' + _joint.name
            else:
                _joint.name = context.active_object.mmd_joint.name_j = '横_' + _joint.name

        return {'FINISHED'}

