bl_info = {
    "name": "vamp",
    "author": "Chris Allen", 
    "version": (1, 2, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "VAMP: Vector Art Motion Processor. Removes back faces.",
    "warning": "Requires one object collection and one camera",
    "wiki_url": "https://github.com/zippy731/vamp",
    "category": "Development",
}

# new 2.93 version:
# - can now use Grease Pencil Line Art as input. Some error checking to ensure GP is baked.
# - output is contained into _vampOutput collection
# this version still compatible w/ 2.8x, but GP Line Art feature only available from 2.93 onward. 

# GOOD TUT: https://blender.stackexchange.com/questions/57306/how-to-create-a-custom-ui
import bpy
import importlib, sys
from bpy.props import IntProperty, EnumProperty, FloatProperty, BoolProperty, StringProperty, PointerProperty
from bpy.types import PropertyGroup, Operator, Panel, Scene
from bpy.app import driver_namespace
from bpy.app.handlers import frame_change_pre, frame_change_post, depsgraph_update_post
import bmesh
import mathutils
from mathutils import Vector, geometry, Matrix
from bpy_extras.object_utils import world_to_camera_view
from math import radians
import time
import random
from random import sample
sys.path.append('.')
from . import fast_vamp_utils
from .fast_vamp_utils import *

global ray_dist # raycast distance
global cast_sens # raycast sensitivity, allows for offset of source vertex
global cam

global edge_sub_unit
global vamp_on 

class OBJECT_OT_vamp_once(bpy.types.Operator):
    bl_label = "VAMP ONCE"
    bl_idname = "render.vamp_once"
    bl_description = "VAMP ONCE"       
    def execute(self, context):
        global cam
        global err_text
        if item_check():
            main_routine()
        else:
            print('item_check failed. :(  ') 
            err_phrase = 'Item check failed.  ' + err_text
            self.report({'WARNING'}, err_phrase)
        return {'FINISHED'}   

class OBJECT_OT_vamp_turn_on(bpy.types.Operator):
    global vamp_on
    bl_label = "Turn on VAMP"
    bl_idname = "render.vamp_turn_on"
    bl_description = "Turn on VAMP"        
    def execute(self, context):
        print("turning vamp on")
        global vamp_on
        scene = context.scene
        vampparams = scene.vamp_params
        print("Hello World")
        print("vamp_target: ", vampparams.vamp_target)

        vamp_on = True
        if item_check():
            pass
        else:
            print('item_check failed. :(  ')  
            vamp_on = False                 
        return {'FINISHED'}
        


        
        
class OBJECT_OT_vamp_turn_off(bpy.types.Operator):
    bl_label = "Turn off VAMP"
    bl_idname = "render.vamp_turn_off"
    bl_description = "Turn off VAMP"        
    def execute(self, context):
        print("turning vamp off")
        global vamp_on
        vamp_on = False                 
        return {'FINISHED'}
        
class OBJECT_OT_trace_turn_on(bpy.types.Operator):
    global trace_on
    bl_label = "Turn on Trace"
    bl_idname = "render.trace_turn_on"
    bl_description = "Turn on Trace"        
    def execute(self, context):
        print("turning Trace on")
        global trace_on
        scene = context.scene
        vampparams = scene.vamp_params
        trace_on = True        
        if item_check():
            pass
        else:
            print('item_check failed. :(  ')  
            trace_on = False                 
        return {'FINISHED'}
        
class OBJECT_OT_trace_turn_off(bpy.types.Operator):
    bl_label = "Turn off TRACE"
    bl_idname = "render.trace_turn_off"
    bl_description = "Turn off Trace"        
    def execute(self, context):
        print("turning trace off")
        global trace_on
        trace_on = False                 
        return {'FINISHED'}

class OBJECT_OT_trace_once(bpy.types.Operator):
    bl_label = "TRACE ONCE"
    bl_idname = "render.trace_once"
    bl_description = "TRACE ONCE"       
    def execute(self, context):
        global cam
        global err_text
        if item_check():
            main_trace_routine()
        else:
            print('item_check failed. :(  ') 
            err_phrase = 'Item check failed.  ' + err_text
            self.report({'WARNING'}, err_phrase)
        return {'FINISHED'}          


class OBJECT_OT_reloadme(bpy.types.Operator):
    # discussion here: https://blender.stackexchange.com/questions/2691/is-there-a-way-to-restart-a-modified-addon
    # discussion/ source here: https://developer.blender.org/T66924   
    bl_label = "Reload Script"
    bl_idname = "render.vamp_reloadme"
    bl_description = "Reload VAMP Script"           
    def execute(self, context):  
        module_name = "vamp_293"   
        mod = sys.modules.get(module_name)
        importlib.reload(mod)  
        re_reg_handler()
        return {'FINISHED'}      
        
class Vamp_PT_Panel(bpy.types.Panel):
    #Creates a Panel in the render context of the properties editor
    bl_label = "VAMP Settings"
    bl_idname = "VAMP_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="OUTLINER_OB_LATTICE")
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        vampparams = scene.vamp_params
        
        row = layout.row()
        sub = row.row()
        sub.scale_x = 2.0
        sub.scale_y = 2.0        
        
        #VAMP ON/OFF
        if vamp_on is True:
            sub.operator("render.vamp_turn_off", text="Turn Off VAMP")            
        else:   
            sub.operator("render.vamp_turn_on", text="Turn On VAMP")
                

        sub.scale_y = 2.0   
        sub.operator("render.vamp_once", text="VAMP ONCE")  
      
        layout.separator()
        
        #user options
        row = layout.row(align=True)
        row.prop(vampparams, "vamp_sil_mode")
        row.prop(vampparams, "vamp_crop_enum")
        
        row = layout.row(align=True)        
        row.prop(vampparams, "vamp_marked_mode")
        row.prop(vampparams, "vamp_crease_mode")
        row.prop(vampparams, "vamp_crease_limit")  
        
        layout.prop(vampparams, "vamp_target")
        layout.prop(vampparams, "vamp_scale")
        layout.prop(vampparams, "vamp_edge_limit")
        
        row = layout.row(align=True)        
        row.prop(vampparams, "vamp_subd_limit")
        row.prop(vampparams, "vamp_edge_subdiv")       
        
        row = layout.row(align=True)
        row.prop(vampparams, "vamp_cull")
        row.prop(vampparams, "vamp_cull_dist")   
        
        row = layout.row(align=True)
        row.prop(vampparams, "vamp_raycast_dist")
        row.prop(vampparams, "vamp_cast_sensitivity")

        row = layout.row(align=True)
        row.prop(vampparams, "vamp_denoise_pass")
        row.prop(vampparams, "vamp_denoise_thresh")
        row.prop(vampparams, "vamp_denoise_pct")   

        #new TRACE options
        row = layout.row()
        sub = row.row()
        sub.scale_x = 2.0
        sub.scale_y = 2.0    
        if trace_on is True:
            sub.operator("render.trace_turn_off", text="Turn Off Trace")            
        else:   
            sub.operator("render.trace_turn_on", text="Turn On Trace")           
        sub.scale_y = 2.0   
        sub.operator("render.trace_once", text="Trace ONCE") 

        row = layout.row(align=True)
        row.prop(vampparams, "vamp_trace_limit")
        
        row = layout.row(align=True)        
        row.prop(vampparams, "vamp_trace_enum")
        row.prop(vampparams, "vamp_trace_curve_enum")
        
        layout.separator()
        # reload this script, re-register app handler
        layout.operator("render.vamp_reloadme", text="Reload Script")
        
class ExitOK(Exception):
    # from https://blender.stackexchange.com/questions/6782/python-command-within-script-to-abort-without-killing-blender
    # usage:  raise ExitOK # quit script immediately
    #print('aborting')
    pass
     


def vamp_handler(scene):    
    global vamp_on
    global cam #te4sti
    global recent_frame
    scene = bpy.data.scenes[0]
    if vamp_on is True:
        if item_check():
            #double check we haven't already vamp'd this frame..
            if scene.frame_current != recent_frame: 
                main_routine()
            else:
                print('***') #something triggered handler again before frame change. skip processing.
            recent_frame = scene.frame_current
        else:
            print('item_check failed. :(  ')      

classes = (OBJECT_OT_vamp_once,OBJECT_OT_vamp_turn_on,OBJECT_OT_vamp_turn_off,OBJECT_OT_trace_once,OBJECT_OT_trace_turn_on,OBJECT_OT_trace_turn_off,OBJECT_OT_reloadme,VampProperties,Vamp_PT_Panel)          

def re_reg_handler():
    #polite app handler management, per:
    #    https://oktomus.com/posts/2017/safely-manage-blenders-handlers-while-developing/
    
    #avoiding dup handlers:
    #  https://blender.stackexchange.com/questions/146837/how-do-i-properly-update-an-application-handler 
    
    handler_key = 'VAMP_293_KEY'
    
    old_vamp_handlers = [h for h in bpy.app.handlers.frame_change_pre
        if h.__name__ == handler_key]
    for v in old_vamp_handlers:
        bpy.app.handlers.frame_change_pre.remove(f)         
    
    if handler_key in driver_namespace:
        if driver_namespace[handler_key] in frame_change_pre:
            frame_change_pre.remove(driver_namespace[handler_key])
        del driver_namespace[handler_key]
    bpy.app.handlers.frame_change_pre.append(vamp_handler) 
    driver_namespace[handler_key] = vamp_handler

def register():
    re_reg_handler()
    
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.vamp_params = PointerProperty(type=VampProperties)  #old 2.79 version 
 
def unregister():
    for cls in reversed(classes):
        # bpy.utils.unregister_class(cls)  
        # polite deregister, per https://blenderartists.org/t/find-out-if-a-class-is-registered/602335
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass    
           

if __name__ == "__main__":
   register()