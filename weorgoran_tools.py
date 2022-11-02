__author__ = "James 'Weorgoran' Smith"
__copyright__ = "Copyright 2022, James Smith"
__credits__ = ["James Smith"]
__license__ = "MIT"
__maintainer__ = "James Smith"
__email__ = "everyonesmells@gmail.com"
__status__ = "Work In Progress"

bl_info = {
    "name": "Weorgoran Tools",
    "description": "Generic Tools Created by Weorgoran",
    "author": "James 'Weorgoran' Smith",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "Toolshelf",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "weorgoran.github.io",
    "category": "Create"}


import bpy
import math


def common_cursor_to_active(angle, sway):
    # Remeber current object.
    print("CURSOR_TO_ACTIVE")
    active_obj = bpy.context.active_object
    active_obj_name = active_obj.name
    #print(active_obj_name)
    
    # Get camera object
    obj_camera = bpy.context.scene.camera

    # Snap to cursor to active object.
    bpy.ops.view3d.snap_cursor_to_active()

    # Add empty at selected object
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', scale=(4, 4, 4))
    obj_empty = bpy.context.active_object
    obj_empty.name = active_obj_name + "_Camera_Control"
    bpy.ops.transform.resize(value=(-2.0, -2.0, -2.0), orient_type='GLOBAL', use_proportional_edit=False, snap=False, use_snap_project=False, use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)

    
    # Parent camera to empty.
    bpy.ops.object.select_all(action='DESELECT') #deselect all object
    #select the object for the 'parenting'
    #object = bpy.data.objects[obj_camera.name]
    obj_camera.select_set(True)
    obj_empty.select_set(True)
  
    #bpy.context.scene.objects.active = obj_empty    #the active object will be the parent of all selected object
    bpy.ops.object.parent_set(keep_transform=True)

    # Animate Camera
    if(sway):
        print("""SWAY""")
        WG_OT_rotate_camera_sway(obj_empty, angle)
    else:
        print("""LOOP""")
        WG_OT_rotate_camera_loop(obj_empty, angle)
    
    return {'FINISHED'}
    
    
def WG_OT_rotate_camera_sway(camera_control, angle):
    view_layer = bpy.context.view_layer
    view_layer.objects.active = camera_control
    
    bpy.context.scene.frame_set(1)
    bpy.ops.anim.keyframe_insert_by_name(type="Rotation")
    bpy.context.scene.frame_set(bpy.context.scene.frame_end)
    bpy.ops.anim.keyframe_insert_by_name(type="Rotation")
    
    
    middle_key_frame = (int)(bpy.context.scene.frame_end/2)
    bpy.context.scene.frame_set(middle_key_frame)
#    view_layer.objects.active = camera_control
    bpy.context.active_object.rotation_mode = 'XYZ'
    bpy.context.active_object.rotation_euler = (0,0,  math.radians(angle)) 
    #bpy.ops.transform.rotate(value=angle, orient_axis='Z', orient_type='GLOBAL')
    bpy.ops.anim.keyframe_insert_by_name(type="Rotation")
    
    return {'FINISHED'}



def WG_OT_rotate_camera_loop(camera_control, angle):
    view_layer = bpy.context.view_layer
    view_layer.objects.active = camera_control
    
    bpy.context.scene.frame_set(1)
    bpy.ops.anim.keyframe_insert_by_name(type="Rotation")


    bpy.context.scene.frame_set(bpy.context.scene.frame_end)
#    view_layer.objects.active = camera_control
    bpy.context.active_object.rotation_mode = 'XYZ'
    bpy.context.active_object.rotation_euler = (0,0,  math.radians(angle)) 
    #bpy.ops.transform.rotate(value=angle, orient_axis='Z', orient_type='GLOBAL')
    bpy.ops.anim.keyframe_insert_by_name(type="Rotation")
    
    
#    bpy.ops.graph.select_all.poll()
#    bpy.ops.action.interpolation_type(type='LINEAR')


    obj = camera_control
    fcurves = obj.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'



    return {'FINISHED'}

# ----------------------------------------- Create a ground plane

class WG_OT_cam_anim_90(bpy.types.Operator):
    """Creates an empty on selected object, binds camera to the empty, and spins the camera 90 degrees."""
    bl_idname = "scene.create_animate_camera90"
    bl_label = "Animate 90"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        print ("can_anim_90 called")
        
        
        common_cursor_to_active(-90, True)
        object = bpy.context.active_object
        #object.scale = (5, 5, 0)#The plane object is created with a size of 2. Scaling it to 10 means to scale it by factor 5
        #bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)# apply scale

        return {'FINISHED'}



# ----------------------------------------- Create a ground plane
class WG_OT_cam_anim_360(bpy.types.Operator):
    """Creates an empty on selected object, binds camera to the empty, and spins the camera 360 degrees."""
    bl_idname = "scene.create_animate_camera360"
    bl_label = "Animate 360"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        print ("can_anim_360 called")
        
        
        common_cursor_to_active(-360, False)
        object = bpy.context.active_object
        #object.scale = (5, 5, 0)#The plane object is created with a size of 2. Scaling it to 10 means to scale it by factor 5
        #bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)# apply scale

        return {'FINISHED'}

#----------------------------------------- Create panel in the toolshelf -------------------------------------------------

class WG_PT_animate_createcamanipanel(bpy.types.Panel):
    bl_label = "Weorgoran Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Animate Camera"

    def draw(self, context):

        # column buttons solution. Less space than single buttons ...
        layout = self.layout
        view = context.space_data
        # Three buttons
        col = layout.column(align=True)
        col.operator("scene.create_animate_camera90", text="Rotate 90")
        col.operator("scene.create_animate_camera360", text="Rotate 360")
# -------------------------------------------------------------------------------------------

# store keymaps here to access after registration
addon_keymaps = []

classes = (WG_OT_cam_anim_90, WG_OT_cam_anim_360, WG_PT_animate_createcamanipanel)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()