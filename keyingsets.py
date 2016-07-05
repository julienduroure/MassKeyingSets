import bpy

class POSE_PT_juks_keying(bpy.types.Panel):
	bl_label = "KeyingSets"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "KeyingSets"

	@classmethod
	def poll(self, context):
		armature = context.object
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def draw(self, context):
		layout = self.layout
		layout.operator("pose.juks_keying", text="Create KeyingSet from selected")

class POSE_OT_juks_keying_from_selected(bpy.types.Operator):
	"""Create/Update KeyingSet from selected"""
	bl_idname = "pose.juks_keying"
	bl_label = "Keying from selected"
	bl_options = {'REGISTER'}

	name = bpy.props.StringProperty(name="",default="KeyingSet from Selection")

	# update   = bpy.props.BoolProperty(default=False) #TODO
	location = bpy.props.BoolProperty(default=True)
	rotation = bpy.props.BoolProperty(default=True)
	scale    = bpy.props.BoolProperty(default=False)
	custom_props = bpy.props.BoolProperty(name="Custom Properties", default=False)
	only_non_locked = bpy.props.BoolProperty(name="Do not key locked channels", default=True)

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.prop(self, "name")
		row = layout.row()
		row.prop(self, "location")
		row.prop(self, "rotation")
		row.prop(self, "scale")
		row = layout.row()
		row.prop(self, "custom_props")
		row = layout.row()
		row.prop(self, "only_non_locked")

	def execute(self, context):
		bones = context.selected_pose_bones
		scene = bpy.context.scene

		ks = scene.keying_sets.new(idname="KeyingSet", name=self.name)
		ks.bl_description = ""

		for bone in bones:
			if self.location == True:
				if self.only_non_locked == True:
					if bone.lock_location[0] == False and bone.lock_location[1] == False and bone.lock_location[2] == False:
						ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.location', index=-1)
					else:
						if bone.lock_location[0] == False:
							ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.location', index=0)
						if bone.lock_location[1] == False:
							ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.location', index=1)
						if bone.lock_location[2] == False:
							ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.location', index=2)
				else:
					ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.location', index=-1)

			if self.rotation == True:
				if bone.rotation_mode == "QUATERNION":
                    if bone.lock_rotation_w == False and bone.lock_rotation[0] == False and bone.lock_rotation[1] == False and bone.lock_rotation[2] == False:
					    ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_quaternion', index=-1)
                    else:
                        if bone.lock_rotation_w == False:
                            ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_quaternion', index=0)
                        if bone.lock_rotation[0] == False:
                            ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_quaternion', index=1)
                        if bone.lock_rotation[1] == False:
                            ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_quaternion', index=2)
                        if bone.lock_rotation[2] == False:
                            ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_quaternion', index=3)
				elif bone.rotation_mode == "AXIS_ANGLE":
                    if bone.lock_rotation_w == False and bone.lock_rotation[0] == False and bone.lock_rotation[1] == False and bone.lock_rotation[2] == False:
					    ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_angle', index=-1)
                    else:
                        if bone.lock_rotation_w == False:
                            ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_angle', index=0)
                        if bone.lock_rotation[0] == False:
                            ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_angle', index=1)
                        if bone.lock_rotation[1] == False:
                            ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_angle', index=2)
                        if bone.lock_rotation[2] == False:
                            ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_angle', index=3)
				else:
					if bone.lock_rotation[0] == False and bone.lock_rotation[1] == False and bone.lock_rotation[2] == False:
					    ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_euler', index=-1)
                    else:
                        if bone.lock_rotation[0] == False:
                            ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_euler', index=0)
                        if bone.lock_rotation[1] == False:
                            ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_euler', index=1)
                        if bone.lock_rotation[2] == False:
                            ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.rotation_euler', index=2)
			if self.scale == True:
				ksp = ks.paths.add(bone.id_data, bone.path_from_id() + '.scale', index=-1)
			if self.custom_props == True:
				for prop in bone.keys():
					if prop != "_RNA_UI":
						ksp = ks.paths.add(bone.id_data, bone.path_from_id() + "[\""+ prop  + "\"]", index=-1)

		return {'FINISHED'}

def register():
	bpy.utils.register_class(POSE_OT_juks_keying_from_selected)
	bpy.utils.register_class(POSE_PT_juks_keying)

if __name__ == "__main__":
	register()
