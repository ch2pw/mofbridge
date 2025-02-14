import bpy
import os
from bpy import context
from bpy.props import StringProperty, BoolProperty
import re  # For cleaning up object names

bl_info = {
    "name": "Blender MOF Bridge",
    "description": "Unwrap your objects with MINISTRY OF FLAT. Hail Ministry of Flat, your flatness!!!",
    "blender": (2, 80, 0),
    "category": "UV",
    "location": "Object > Unwrap in Ministry of Flat",
    "version": (1, 1),
    "author": "rentanek0",
    "doc_url": "https://www.quelsolaar.com/ministry_of_flat/",
    "tracker_url":"https://www.quelsolaar.com/ministry_of_flat/",
}

class MyAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    folder_path: StringProperty(
        name="MOF folder",
        description="Enter the path to the folder containing Ministry of Flat",  # Enter the path to the folder containing Ministry of Flat
        subtype="DIR_PATH",
    )

    separate: BoolProperty(
        name="Separate edges. Guarantees that all hard edges are separated. Useful for lightmapping and Normalmapping",
        default=True,
    )

    pack: BoolProperty(
        name="Pack after unwrap. (Packing in blender)",
        default=True,
    )

    showUV: BoolProperty(
        name="Show UV when done. (Goes to edit mode)",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "folder_path")
        layout.prop(self, "separate")
        layout.prop(self, "pack")
        layout.prop(self, "showUV")

class AutoUV(bpy.types.Operator):
    """Uses Ministry of Flat to automatically perform UV unwrapping"""  # Description shown on hover

    bl_idname = "object.autouv"  # Operator ID (must be in lowercase)
    bl_label = "Unwrap in Ministry of Flat"  # Name displayed in the UI
    bl_options = {"REGISTER"}

    def execute(self, context):  # Main operator logic
        # Step 1: Export selected objects
        active_object = context.active_object
        selected_objects = context.selected_objects  # Get all selected objects
        if not selected_objects:
            self.report({"ERROR"}, "No objects selected!")  # Error if no objects are selected
            return {"CANCELLED"}

        # Save original object names
        #original_names = {obj: obj.name for obj in selected_objects}

        # Export all selected objects to a single .obj file
        fn = os.path.join(bpy.app.tempdir, "exported_objects.obj")  # Temporary export file
        bpy.ops.wm.obj_export(
            filepath=fn,
            export_selected_objects=True,  # Export only selected objects
            export_materials=False,  # Do not export materials
            apply_modifiers=False,  # Do not apply modifiers
        )

        # Renaming original objects so imported objects can keep their names
        suffix = "_1ja"
        for obj in selected_objects:
            obj.name = obj.name + suffix        


        # Step 2: Run Ministry of Flat for UV unwrapping
        fn2 = os.path.join(bpy.app.tempdir, "unpacked_objects.obj")  # Temporary output file
        preferences = context.preferences.addons[__name__].preferences
        folder_path = preferences.folder_path  # Path to Ministry of Flat
        path = os.path.join(folder_path, "UnWrapConsole3.exe")

        separate = "TRUE" if preferences.separate else "FALSE" #separate edges or not
        os.system(f"{path} {fn} {fn2} -CUTDEBUG FALSE -SEPARATE {separate}")  # Run Ministry of Flat

        # Step 3: Import the result of UV unwrapping
        bpy.ops.wm.obj_import(filepath=fn2)

        # Step 4: Restore original names for imported objects
        imported_objects = context.selected_objects  # Get all imported objects

        # Step 5: Copy UV maps from imported objects to the original objects
        for obj in selected_objects:
            for imported_obj in imported_objects:
                if imported_obj.name + suffix == obj.name:  # Match by original name including suffix
                    # Check if both objects have UV layers
                    if obj.data.uv_layers and imported_obj.data.uv_layers:
                        # Remove all existing UV layers from the original object
                        while obj.data.uv_layers:
                            obj.data.uv_layers.remove(obj.data.uv_layers[0])

                        # Copy UV layers from the imported object to the original object
                        for src_uv in imported_obj.data.uv_layers:
                            new_uv = obj.data.uv_layers.new(name=src_uv.name)
                            
                            # Create an array to store UV coordinates
                            uv_coords = [0.0] * (len(src_uv.data) * 2)  # 2 values (u, v) per vertex
                            
                            # Get UV coordinates from the source UV layer
                            src_uv.data.foreach_get("uv", uv_coords)
                            
                            # Set UV coordinates in the new UV layer
                            new_uv.data.foreach_set("uv", uv_coords)

        # Step 6: Delete all imported objects
        for imported_obj in imported_objects:
            bpy.data.objects.remove(imported_obj)

        for obj in selected_objects:
            obj.name = obj.name.removesuffix(suffix)
            obj.select_set(True)  

        bpy.context.view_layer.objects.active = active_object

        # Step 7: Clean up temporary files
        os.remove(fn)
        os.remove(fn2)

        if preferences.pack:
            wm = bpy.context.window_manager
            wm.progress_begin(0, 99)
            wm.progress_update(77)
            # Step 6: Pack UV islands
            bpy.ops.object.mode_set(mode='EDIT')  # Switch to Edit Mode
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.context.area.ui_type = 'UV'
            bpy.ops.uv.select_all(action='SELECT')  # Select all UVs
            #bpy.ops.uv.pack_islands()
            bpy.ops.uv.pack_islands(margin=0.001)  # Pack UV islands with a margin of 0.001
            bpy.context.area.type = 'VIEW_3D'
            bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to Object Mode
            wm.progress_end()

        if preferences.showUV: bpy.ops.object.mode_set(mode='EDIT')            

        self.report({'INFO'}, f"Processing complete. ")

        return {"FINISHED"}  # Operation completed


def menu_func(self, context):
    self.layout.operator(AutoUV.bl_idname)  # Add operator to the menu


def register():
    bpy.utils.register_class(MyAddonPreferences)
    bpy.utils.register_class(AutoUV)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Add item to the object menu


def unregister():
    bpy.utils.unregister_class(MyAddonPreferences)
    bpy.utils.unregister_class(AutoUV)
    bpy.types.VIEW3D_MT_object.remove(menu_func)  # Remove item from the object menu


if __name__ == "__main__":
    register()
