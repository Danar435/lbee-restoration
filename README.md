# LBEE Restoration Patch

Restoring Little Busters' original assets!

This patch is aimed at the Steam version of Little Busters, namely English Edition, which a port created by Prototype, using Luca Engine. These ports are notorious for having a bland UI and cut backgrounds/CGs due to the 16:9 aspect ratio. Well, that is no longer the case. With the patch...

- The game window is set to 4:3
- Backgrounds are restored 
- CGs are restored
- Some CGs are also uncensored
- Textboxes are made to look like the original
- Menus follow the light blue LB theme
- Komari's "donut scene" is restored
- Characters are slightly taller

There are some things that were not restored to 4:3, namely the battle and the baseball minigames, with the battle minigame being a bit zoomed in.

Because this is just an asset replacement patch, there is a limit to what I can do. Minigames and other events require a decompilation of the engine to manipulate the positioning of the UI and text elements, which is out of scope for this project. I've done as much as I can do with the tools I was given.

## Screenshots

<p align="center">
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/assets/SS1.png">
    <img src="assets/SS1.png" alt="Main Menu" width="300"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/assets/SS2.png">
    <img src="assets/SS2.png" alt="In-game" width="300"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/assets/SS3.png">
    <img src="assets/SS3.png" alt="CGs" width="300"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/assets/SS4.png">
    <img src="assets/SS4.png" alt="Events" width="300"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/assets/SS5.png">
    <img src="assets/SS5.png" alt="Choices" width="300"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/assets/SS6.png">
    <img src="assets/SS6.png" alt="Battles" width="300"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/assets/SS7.png">
    <img src="assets/SS7.png" alt="Rankings" width="300"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/assets/SS8.png">
    <img src="assets/SS8.png" alt="Baseball" width="300"/>
  </a>
</p>

## Installing

[Click here to download the patch](http://github.com/Danar435/lbee-restoration/releases/latest/download/lbee-patch.zip), or download it from the [releases tab](https://github.com/Danar435/lbee-restoration/releases)!

After downloading, extract the zip file and copy its contents to `C:\Program Files (x86)\Steam\steamapps\common\Little Busters! English Edition`, or wherever you have installed the game. If you're not sure, then you can right click the game from within Steam and then click on `Manage > Browse local files`.

Windows will ask you if you want to overwrite the files. You can just click on yes. If you don't want to redownload the game in case you're unhappy with the patch, you can instead create a copy (backup) of the `files` folder and the `system.cnf` file, and then paste in the patch. If you overwrote the files and want to remove the patch, you can right click on the game in Steam, then go to `Properties`. From there go to `Installed Files` and then `Verify integrity of game files`. This will redownload all of the files that the patch replaced.

## Building

You can use LuckSystem to repack the pak files. I've made a bash script to automate the process. You will need the LuckSystem binary in the same folder as the patch, or alternatively you can modify the bash script.

`./lbee-repack.sh path/to/game/folder` 

This will create a folder containing the patch same folder as the script.

## Notes

I've made some notes for those looking into making a similar patch or contribute to this. You can [find them here](http://github.com/Danar435/lbee-restoration/blob/main/NOTES.md). If you have any questions regarding the process, then please use GitHub's Discussions instead of opening Issues.

## Credits

- LuckSystem
- Lbee-utils
- Zipplet/Kotomi
- Sep7
