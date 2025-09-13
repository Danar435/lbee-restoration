# Notes

Just a text dump with some info on the tools, paks and processes used for this project. Hope you find them useful.

## Terminology 

There are 5 distinct steps for the process, and I'll be referring to each step by the following names, coming mostly from LuckSystem.

Original (pak) - unpacked (cz) - extracted (png) - modified (png) -
imported (cz) -
repacked (pak)

## Tools

There are a number of tools used for this project, and none of them are perfect.

### LuckSystem

Used for unpacking and repacking pak files. 

`lucksystem pak extract -s INPUT.PAK -i INPUT.PAK -o out.txt -a output`
`lucksystem pak replace -s INPUT.PAK -i output -o OUTPUT.PAK`

Make sure that the output folder exists beforehand.
It can also handle images, but it doesn't properly extract some images. As for importing images, you need to make sure that the size in the source header matches the size of the image beforehand and after importing you need to decrease the byte at offset by 1 for some reason.

### Lbee-utils

Used for extracting and importing images.  

`lbee-czutil decode ...`
`lbee-czutil replace ...`

When changing the size of an image, it automatically changes the size in the header, but doesn't change the crop or coordinates. This can be useful, but you'll need to manually change them accordingly. There is also a pak tool, but I can't get it to work properly.

### Lbee script 

Used for editing the script. This one is actually pretty nice.

`python folder/unpack.py`
`cp script/file folder/script`
python folder/repack.py

LuckSystem also supports extracting the script (in theory), but good luck with that.

### Patch.py

My own script that has some commands for dealing with annoying tasks or executing batch actions. You may find some use in it.

`not yet done`

## Paks

That's where the assets are stored. There are tools to unpack and repack those archives, but current ones don't unpack all metadata.

### BGCG

Contains all the backgrounds. Unlike the CGs they are all in 16:9 aspect ratio, so I had to dig through and upscale the original assets for this patch. Some backgrounds needed coordinate adjustments, but for the most part the 'bg' file should work as a source for importing.

### EVENTCG

Contains all the CGs. When you extract them you'll notice that some images are cut, which was done to save space. The cut images are overlaid on top of the full size CGs in-game according to specific coordinates in the header that indicate where they should be placed. I made a command to extract those images in full size.

Command

And another to merge the overlay with the base image.

Command

But since most of them are in 4:3, they didn't need much work, if any, for this patch. I've only restored some of the CGs to the original. Longer CGs needed coordinate adjustments, but again, 'bg' should work as a source for importing for most images, given that they're full size.

### CHARCG

Contains character images. Like with the CGs, the faces are cut out and overlaid on top of a base image. It's a bit difficult to figure out which image from just looking at the pak, so I suggest either loading the image in the script (what I did) or copy my homework and look inside of `charcg-raw`. While repacking the full images is a decent option (what I did with eventcg), there are some semi-transparent pixels around the image, which are stacked when the images are overlaid on top of each other. To circumvent that I made a command to upscale (using nearest neighbour) the original cut assets and use them to select and delete the empty space on the new assets.

Command

Note that there may be some issues with images xx, xx, so I suggest editing the script or doing them manually. As for importing, the anchor seems to be in a different spot, so use 'char' as a source for full size images.

### GENCG

Contains backgrounds, CGs and characters with sepia and b/w filter on top, used for flashback sequences. To replicate the sepia filter, decrease the contrast by 25 and apply a yellow-ish layer on top with color burn blend. For b/w images, just use a black layer instead. #F3D7C7

### OTHCG

Contains images that you see from time to time in-game, such as visual effects, assets for minigames and EDs. A lot of them just needed to be moved, which I've done with the coordinates in the header. When importing images I'd suggest to just use the original unpacked image as a base and changing the size in the header afterwards.

### PARTS

Contains some in-game UI elements, such as the date and textbox. Similarly to othcg, I'd recommend using the original assets as source.

### SYSCG

Contains menu and some UI elements. There seems to be some weirdness when it comes to converting images from syscg, because the main menu seems to fail to load if the size of the pak is bigger than the original. Luckily the menu images are cz0 (uncompressed) and converting them to cz3 seems to work just fine.