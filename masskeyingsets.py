#
# MassKeyingSets is part of BleRiFa. http://BleRiFa.com
#
##########################################################################################
#	GPL LICENSE:
#-------------------------
# This file is part of MassKeyingSets.
#
#    MassKeyingSets is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MassKeyingSets is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MassKeyingSets.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################################
#
#	Copyright 2016-2017 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################

bl_info = {
	"name": "Mass KeyingSets",
	"author": "Julien Duroure",
	"version": (0, 1, 0),
	"blender": (2, 77, 0),
	"location": "Scene properties",
	"warning": "Beta version",
	"description": "Mass KeyingSets creation from Selection",
	"wiki_url": "http://blerifa.com/tools/MassKeyingSets/",
	"tracker_url": "https://github.com/julienduroure/MassKeyingSets/issues/",
	"category": "Animation"}

import bpy

def check_case(context):
	#Armature in pose mode
	if len(context.selected_objects) == 1 and context.selected_objects[0].type == 'ARMATURE' and context.mode == 'POSE' and len(context.selected_pose_bones) != 0:
		return True, 'BONES'
	elif len(context.selected_objects) != 0 and context.mode == 'OBJECT':
		# Objects
		types = [obj.type for obj in context.selected_objects]
		if 'ARMATURE' in types:
			types.remove('ARMATURE')
		if len(types) != 0:
			return True, 'OBJ'

	# poll KO
	return False, 'DUMMY'

class POSE_PT_juks_keying(bpy.types.Panel):
	bl_label = "Mass KeyingSets creation"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"

	@classmethod
	def poll(self, context):
		return check_case(context)[0]

	def draw(self, context):
		layout = self.layout
		layout.operator("pose.juks_keying", text="Mass KeyingSets creation")

class POSE_OT_juks_keying_from_selected(bpy.types.Operator):
	"""Create/Update KeyingSet from selected"""
	bl_idname = "pose.juks_keying"
	bl_label = "MassKeyingSets"
	bl_options = {'REGISTER'}

	name = bpy.props.StringProperty(name="",default="MassKeyingSets")

	update   = bpy.props.BoolProperty(default=False)
	location = bpy.props.BoolProperty(default=True)
	rotation = bpy.props.BoolProperty(default=True)
	scale    = bpy.props.BoolProperty(default=False)
	bone_custom_props = bpy.props.BoolProperty(name="Bone Custom Properties", default=False)
	obj_custom_props  = bpy.props.BoolProperty(name="Object Custom Properties", default=False)
	data_custom_props  = bpy.props.BoolProperty(name="Object Data Custom Properties", default=False)
	only_non_locked = bpy.props.BoolProperty(name="Do not key locked channels", default=True)

	@classmethod
	def poll(self, context):
		return check_case(context)[0]

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.prop(self, "update", text="Update KeyingSet if already exists")
		row = layout.row()
		row.prop(self, "name")
		row = layout.row()
		row.prop(self, "location")
		row.prop(self, "rotation")
		row.prop(self, "scale")
		row = layout.row()
		if check_case(context)[1] == "BONES":
			row.prop(self, "bone_custom_props")
		else:
			row.prop(self, "obj_custom_props")
			row = layout.row()
			row.prop(self, "data_custom_props")
		row = layout.row()
		row.prop(self, "only_non_locked")

	def execute(self, context):
		if check_case(context)[1] == "BONES":
			bones = context.selected_pose_bones
			scene = bpy.context.scene

			if self.update == False:
				ks = scene.keying_sets.new(idname="KeyingSet", name=self.name)
				ks.bl_description = ""
			else:
				if self.name not in scene.keying_sets.keys():
					self.report({'WARNING'}, "KeyingSet not exists!")
					return {'CANCELLED'}
				ks = scene.keying_sets[self.name]

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
				if self.bone_custom_props == True:
					for prop in bone.keys():
						if prop != "_RNA_UI":
							ksp = ks.paths.add(bone.id_data, bone.path_from_id() + "[\""+ prop  + "\"]", index=-1)

		elif check_case(context)[1] == "OBJ":
			scene = context.scene
			ks = scene.keying_sets.new(idname="KeyingSet", name=self.name)
			ks.bl_description = ""

			armature_found = False
			for obj in context.selected_objects:
				if obj.type != "ARMATURE":
					if self.location == True:
						if self.only_non_locked == True:
							if obj.lock_location[0] == False and obj.lock_location[1] == False and obj.lock_location[2] == False:
								ksp = ks.paths.add(obj, 'location', index=-1)
							else:
								if obj.lock_location[0] == False:
									ksp = ks.paths.add(obj, 'location', index=0)
								if obj.lock_location[1] == False:
									ksp = ks.paths.add(obj, 'location', index=1)
								if obj.lock_location[2] == False:
									ksp = ks.paths.add(obj, 'location', index=2)
						else:
							ksp = ks.paths.add(obj, 'location', index=-1)

					if self.rotation == True:
						if obj.rotation_mode == "QUATERNION":
							if obj.lock_rotation_w == False and obj.lock_rotation[0] == False and obj.lock_rotation[1] == False and obj.lock_rotation[2] == False:
								ksp = ks.paths.add(obj, 'rotation_quaternion', index=-1)
							else:
								if obj.lock_rotation_w == False:
									ksp = ks.paths.add(obj, 'rotation_quaternion', index=0)
								if obj.lock_rotation[0] == False:
									ksp = ks.paths.add(obj, 'rotation_quaternion', index=1)
								if obj.lock_rotation[1] == False:
									ksp = ks.paths.add(obj, 'rotation_quaternion', index=2)
								if obj.lock_rotation[2] == False:
									ksp = ks.paths.add(obj, 'rotation_quaternion', index=3)
						elif obj.rotation_mode == "AXIS_ANGLE":
							if obj.lock_rotation_w == False and obj.lock_rotation[0] == False and obj.lock_rotation[1] == False and obj.lock_rotation[2] == False:
								ksp = ks.paths.add(obj, 'rotation_angle', index=-1)
							else:
								if obj.lock_rotation_w == False:
									ksp = ks.paths.add(obj, 'rotation_angle', index=0)
								if obj.lock_rotation[0] == False:
									ksp = ks.paths.add(obj, 'rotation_angle', index=1)
								if obj.lock_rotation[1] == False:
									ksp = ks.paths.add(obj, 'rotation_angle', index=2)
								if obj.lock_rotation[2] == False:
									ksp = ks.paths.add(obj, 'rotation_angle', index=3)
						else:
							if obj.lock_rotation[0] == False and obj.lock_rotation[1] == False and obj.lock_rotation[2] == False:
								ksp = ks.paths.add(obj, 'rotation_euler', index=-1)
							else:
								if obj.lock_rotation[0] == False:
									ksp = ks.paths.add(obj, 'rotation_euler', index=0)
								if obj.lock_rotation[1] == False:
									ksp = ks.paths.add(obj, 'rotation_euler', index=1)
								if obj.lock_rotation[2] == False:
									ksp = ks.paths.add(obj, 'rotation_euler', index=2)
					if self.scale == True:
						ksp = ks.paths.add(obj, 'scale', index=-1)
					if self.obj_custom_props == True:
						for prop in obj.keys():
							if prop != "_RNA_UI":
								ksp = ks.paths.add(obj, "[\""+ prop  + "\"]", index=-1)
					if self.data_custom_props == True:
						for prop in obj.data.keys():
							if prop != "_RNA_UI":
								ksp = ks.paths.add(obj.data, "[\""+ prop  + "\"]", index=-1)
				else:
					armature_found = True
			if armature_found == True:
				self.report({'WARNING'}, "Armatures not taken into account")

		return {'FINISHED'}

def register():
	bpy.utils.register_class(POSE_OT_juks_keying_from_selected)
	bpy.utils.register_class(POSE_PT_juks_keying)

def unregister():
	bpy.utils.unregister_class(POSE_OT_juks_keying_from_selected)
	bpy.utils.unregister_class(POSE_PT_juks_keying)

if __name__ == "__main__":
	register()
