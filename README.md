# ZERO Sievert Sprite Tool #

This is a modding tool for ZERO Sievert that extracts PNG images from the compressed binary and allows for repacking edited PNG images.

This tool was created for version 0.26.2 of ZERO Sievert, but will likely work on future versions with minimal updating.

This tool may also work for other Game Maker engine games, but no support is guaranteed.

### Requirements ###

* Python 3.11.0

### How To Use ###

- Extract 'ZS_sprite_tool.py' to an unprotected folder (NOT within Program Files, etc)
- Copy 'data.win' from your ZERO Sievert game folder, paste it next to 'ZS_sprite_tool.py'.

For unpacking:
- Drag and drop 'data.win' onto 'ZS_sprite_tool.py' and wait for the unpacking to complete.

You can now edit the PNG files within the 'output' folder freely with a program such as GIMP or Photoshop. Please ensure the files are saved with transparency and are compressed. 

For repacking:
- Drag and drop the folder 'output' onto 'ZS_sprite_tool.py' and wait for the packing to complete.
- Original file will be named 'data.backup', modded file will be named 'data.win'.
- Copy and paste 'data.win' into your ZERO Sievert game folder, replace the file within (create a backup if desired).

NOTE: The file size for each PNG must be smaller than the original file. Through my tests, any file saved through Adobe Photoshop with compression enabled came out substantially smaller.

Do NOT rename any of the PNG files, and do NOT delete 'repackinfo' within the output folder.

### Contact ###

* RaiRaiTheRaichu#1005 on Discord.