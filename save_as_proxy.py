bl_info = {
    "name": "Save File by proxy",
    "author": "Wouter Vandenneucker",
    "version": (1,1),
    "blender": (2, 80, 0),
    "location": "ctrl+s / cmd+s",
    "description": "Saves the blendfile to a temporary location before copying to final location. Works by bypassing the ctrl+s or cmd+s command.",
    "warning": "Runs user specified python code",
    "wiki_url": "#",
    "tracker_url": "https://github.com/woutervddn/blender_addon_save_by_proxy/issues",
    "category": "System",
}

import bpy
import os
import shutil
import time, datetime

def _copyfileobj_patched(fsrc, fdst, length=16*1024*1024):
    """Patches shutil method to hugely improve copy speed"""
    while 1:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
shutil.copyfileobj = _copyfileobj_patched


class ProxyFileSave(bpy.types.Operator):
    """Set a filename prefix before saving the file"""
    #bl_idname = "wm.save_proxy"
    
    bl_label = "Save Proxied Blendfile"
    bl_idname = "file.save_as_proxy"

    def execute(self, context):
        if( bpy.data.filepath != '' and bpy.data.is_saved != False):
            print("SAVING BY PROXY")
            outname = bpy.path.basename(bpy.data.filepath)
            outpath = os.path.dirname( bpy.path.abspath( bpy.context.preferences.filepaths.temporary_directory ) )
            outpath_final = os.path.dirname(bpy.path.abspath(bpy.data.filepath))
            print(os.path.join(outpath, outname))
            report = bpy.ops.wm.save_as_mainfile(filepath=os.path.join(outpath, outname),
                        check_existing=True, copy=True)
                        
            # os.rename(os.path.join(outpath, outname), os.path.join(outpath_final, outname)) # Does not work accross devices
            if report == {"FINISHED"}:
                shutil.move(os.path.join(outpath, outname), os.path.join(outpath_final, outname))
                return {"FINISHED"}
            else:
                return report
        else:
            print("Initial file wasn't saved yet; omitting save by proxy")
            return bpy.ops.wm.save_mainfile('INVOKE_AREA')

# def menu_save_proxy(self, context):
#    print("hello_world")
    
#    self.layout.operator(ProxyFileSave.bl_idname)
                

def register():
    # bpy.utils.register_module(__name__)
    
    from bpy.utils import register_class
    register_class(ProxyFileSave)

    # add the menuitem to the top of the file menu
    # bpy.types.TOPBAR_MT_file_new.append(menu_save_proxy)

    wm = bpy.context.window_manager
    win_keymaps = wm.keyconfigs.user.keymaps.get('Window')
    if win_keymaps:
        # disable standard save file keymaps
        for kmi in win_keymaps.keymap_items:
            if kmi.idname == 'wm.save_mainfile':
                kmi.active = False

        # add a keymap for our save operator
        kmi = win_keymaps.keymap_items.new(ProxyFileSave.bl_idname, 'S', 
                    'PRESS', ctrl=True)

def unregister():

    wm = bpy.context.window_manager
    win_keymaps = wm.keyconfigs.user.keymaps.get('Window')
    if win_keymaps:
        for kmi in win_keymaps.keymap_items:
            # re-enable standard save file
            if kmi.idname == 'wm.save_mainfile':
                kmi.active = True
            if kmi.idname == ProxyFileSave.bl_idname:
                win_keymaps.keymap_items.remove(kmi)

    # bpy.types.TOPBAR_MT_file_new.remove(menu_save_proxy)

    # bpy.utils.unregister_module(__name__)
    
    from bpy.utils import unregister_class
    unregister_class(ProxyFileSave)

if __name__ == "__main__":
    register()
