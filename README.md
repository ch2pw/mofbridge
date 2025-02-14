# Blender Ministry of Flat Bridge Addon

This addon serves as a bridge between Blender and the **Ministry of Flat** UV unwrapping tool, available at [https://www.quelsolaar.com/ministry_of_flat/](https://www.quelsolaar.com/ministry_of_flat/). It automates the process of exporting objects from Blender, unwrapping their UVs using Ministry of Flat, and reimporting the results back into Blender. The initial version for this addon was written in the article [https://techracho.bpsinc.jp/ecn/2024_08_22/144348](https://techracho.bpsinc.jp/ecn/2024_08_22/144348) by [@techracho](https://x.com/techracho). 

## Installation

1. Download the `.py` file for the addon.
2. Open Blender and go to `Edit > Preferences > Add-ons`.
3. Click `Install...` and select the downloaded `.py` file.
4. Enable the addon by checking the box next to it.
5. Select the path to Ministry of Flat executables directory.

---

## Usage

1. Select one or more objects in Blender.
2. Go to the `Object` menu in the 3D Viewport.
3. Click `Unwrap in Ministry of Flat` to start the process.
4. The addon will export the objects, unwrap their UVs using Ministry of Flat, and reimport the results.

---

## Addon Settings

The addon provides several settings to customize its behavior:

### `MOF folder`
- **Description**: The path to the folder containing the Ministry of Flat executable (`UnWrapConsole3.exe`).
- **Purpose**: Specifies where the addon should look for the Ministry of Flat tool.

### `Separate edges`
- **Description**: Guarantees that all hard edges are separated. Useful for lightmapping and normal mapping.
- **Default**: `True`
- **Purpose**: Ensures clean UV seams for specific use cases like baking.

### `Pack after unwrap`
- **Description**: Automatically packs UV islands after unwrapping. This uses Blender's built-in UV packing functionality.
- **Default**: `True`
- **Purpose**: Optimizes UV space usage by packing the islands efficiently.

### `Show UV when done`
- **Description**: Switches to UV editing mode after the process is complete.
- **Default**: `True`
- **Purpose**: Allows you to immediately inspect the UV maps in the UV Editor.

---

## Workflow

1. **Export**: The selected objects are exported to a temporary `.obj` file.
2. **Unwrap**: Ministry of Flat processes the `.obj` file and generates a new file with unwrapped UVs.
3. **Import**: The unwrapped objects are imported back into Blender.
4. **Copy UVs**: The UV maps from the imported objects are copied to the original objects.
5. **Cleanup**: Temporary files and imported objects are removed.

---

## Notes

- **Ministry of Flat**: This addon relies on the Ministry of Flat tool, which must be downloaded and installed separately from [https://www.quelsolaar.com/ministry_of_flat/](https://www.quelsolaar.com/ministry_of_flat/).
- **Blender Compatibility**: The addon is designed for Blender 2.80 and above.
- **Feedback**: For questions or feedback, contact me on X (formerly Twitter): [@rentaneko3d](https://x.com/rentaneko3d).

---

## Credits

- **Ministry of Flat**: Developed by [Quel Solaar](https://www.quelsolaar.com/).
- **Inspiration**: The initial version for this addon was written in the article [https://techracho.bpsinc.jp/ecn/2024_08_22/144348](https://techracho.bpsinc.jp/ecn/2024_08_22/144348).
- **Developer**: [@rentaneko3d](https://x.com/rentaneko3d).

Make The Earth Flat Again.
---

## License

This addon is provided under the MIT License. Feel free to modify and distribute it as needed.
