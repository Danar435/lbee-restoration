# Notes

Just a text dump with some info on the tools, paks and processes used for this project. Hope you find them useful.

## Terminology 

There are 5 distinct steps for the process, and I'll be referring to each step by the following names, coming mostly from LuckSystem. The names could refer to either a single file or to a folder containing mutliple files. Folders are denoted with a slash at the end of the name.

```
Original (pak) -> unpacked (cz) -> extracted (png) -> modified (png) -> imported (cz) -> repacked (pak)
```



## Tools

There are a number of tools used for this project, and none of them are perfect.

### LuckSystem

Used for unpacking and repacking pak files. 

```bash
lucksystem pak extract -s INPUT.PAK -i INPUT.PAK -o out.txt -a unpacked/
```
```bash
lucksystem pak replace -s INPUT.PAK -i imported/ -o OUTPUT.PAK
```

Make sure that the output folder exists beforehand.

LuckSystem can also handle images, but the process is more annoying. It also doesn't properly extract some images. As for importing images, you need to make sure that the size in the source header matches the size of the image beforehand and after importing you need to decrease the byte at offset `0x24` by 1 for some reason. See what I mean by annoying?

### lbee-utils

Used for extracting and importing images.  

```bash
lbee-czutil decode unpacked extracted.png
```
```bash
lbee-czutil replace unpacked modified.png imported
```

When changing the size of an image, it automatically changes the dimensions in the header, but doesn't change the crop or bounds. This is partially convenient, but you'll need to manually change them accordingly. In most cases the crop and bounds are the same as the size, so I'd usually copy the dimensions at offset `0x08-0x0B` to `0x14-0x17` and `0x18-0x1B`. You can also manipulate the x coordinates at offset `0x10-0x11` and y coordinates at offset `0x12-0x13`. More information on how the header works [here](https://g2games.dev/blog/2024/06/28/the-cz-image-formats/).

There is also a pak tool, but I can't get it to work properly.

### LB_repack 

Used for editing the script. This one is actually pretty nice, except that there is an initial setup.

```bash
  cd LB_repack
  mkdir -p ./core
  mkdir -p ./SCRIPT
  mv ./steam/*.py ./
  mv ./steam/core/opcode_steam.txt ./core/opcode_steam.txt
  cp /path/to/SCRIPT.PAK ./SCRIPT/SCRIPT_steam.PAK
```

Afterwards it's really simple to use.

```bash
  python3 unpack.py 
```
```bash
  python3 repack.py
```

It will create a `disassembled` folder in the `SCRIPT`, which has the extracted script. Repacking it will create `SCRIPT_repacked.PAK` in the same folder

LuckSystem also supports extracting the script (in theory), but good luck with that.

### Helper.py

My own script that has some commands for dealing with annoying tasks or executing batch actions. More information can be found in the file itself. 

## Paks

That's where the assets are stored. There are tools to unpack and repack those archives, but current ones don't unpack all metadata.

### BGCG

Contains all the backgrounds. Unlike the CGs they are all in 16:9 aspect ratio, so I had to dig through and upscale the original assets for this patch. When using lbee-czutil to replace the images (so long they're the same size), you can use the same unpacked image that has the crop and bounds set beforehand. This speeds up the process. Some backgrounds needed coordinate adjustments.

### EVENTCG

Contains all the CGs. When you extract them you'll notice that some images are cut, which was done to save space. The cut images are overlaid on top of the full size CGs in-game according to the coordinates in the header that indicate where they should be placed. Since most of them are in 4:3, they didn't need much work, if any, for this patch. I've only restored some of the CGs to the original. Longer CGs needed coordinate adjustments.

### CHARCG

Contains character images. Like with the CGs, the faces are cut out and overlaid on top of a base image. It's a bit difficult to figure out which image from just looking at the pak, so I suggest either loading the image in the script (what I did) or copy my homework and look inside of `assets/charcg-raw`. Repacking the full images is a decent option (what I did with eventcg), but there are some semi-transparent pixels around the image, which are stacked when the images are overlaid on top of each other. I originally cut the images similar to how they are extracted, and while it looked good, when a character moves or scales, you could see a faint outline. So instead I dug through the pak file and found where the overlays are assigned and removed all of that (you can see it in the shell script), and just used the full size images.

### GENCG

Contains backgrounds, CGs and characters with sepia and b/w filter on top, used for flashback sequences. Same steps as for the previous 3 paks. To replicate the sepia filter, decrease the contrast by 25 and apply a yellow-ish layer (#F3D7C7) on top with color burn blend. For b/w images, just use a black layer instead. 

### OTHCG

Contains images that you see from time to time in-game, such as visual effects, assets for minigames and EDs. What you need to do varies a lot case by case, but a lot of them just needed to be moved, which I've done with the coordinates in the header. This is really the most annoying pak of them all.

### PARTS

Contains some in-game UI elements, such as the date and textbox. Not much to say here.

### SYSCG

Contains menu and some UI elements. There seems to be some weirdness when it comes to converting images from syscg, because the main menu fails to load if the size of the pak is larger than the original. Luckily the menu images are cz0 (uncompressed) and converting them to cz3 seems to work just fine. 

On that note, a similar behaviour happened when the game called the final backrgound from BGCG. This time the images are compressed, but I mitigated the issue by never calling that background and instead calling a different image in the script. I'm not sure if this is something universal between the paks or a one off thing.

## Videos

You can't just replace a video in Luca Engine with another, it'll simply fail to load. Even if you're using the same codecs and the same settings, the game will just freeze. At least it's smart enough to skip the video if it doesn't exist. But anyways, evidently I managed to replace the videos, and the way I did it was painful to say the least.

First you'll need to install the [WebM DirectShow Filters](https://www.free-codecs.com/webm_directshow_filters_download.htm) on your Windows system, which includes the encoder that Prototype used to make the videos. There seems to be very few software that can use DirectShow filters, but I went for [GraphStudioNext](https://github.com/cplussharp/graph-studio-next). It looks very outdated and it is a bit clunky (that seems to be a pattern here), but it got the job done. The videos are made using "webmmux", but I noticed that just using the muxer isn't enough, I also had to encode it using the VP8 filter included in the codecs. The issue I had was that almost nothing could feed into the encoder, that is except for MPEG1 decodes... Yuck. So that's why the videos look a bit worse than they did before.

The final patchbay looked like this:
<a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/.github/assets/graph.png">
<img src=".github/assets/graph.png" alt="Graph"/>
