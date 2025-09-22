# LBEE Restoration Patch

Restore Little Busters' original assets!

This patch is aimed at the Steam version of Little Busters: English Edition, a port created by Prototype using the Luca Engine. These ports are notorious for having a bland UI and cut backgrounds/CGs due to the 16:9 aspect ratio. Well, that is no longer the case. With this patch...

- The game window is set to 4:3
- Backgrounds are restored to 4:3
- CGs are restored to 4:3
- CGs are uncensored like the original (Optional)
- Komari's "donut scene" is restored (Optional)
- Textboxes are changed to look like the original
- Revamped some menus like the original
- Characters are slightly taller
- The original OP is back! (set movie quality to low under system in game settings)

Do note that the patch is uncensored by default to the levels of the original VN, not of Ecstasy. 

Some elements could not be restored to 4:3, specifically the battle and baseball minigames, with the battle minigame appearing slightly zoomed in. Additionally, certain elements like the 'status' card images are now broken.

Because this is an asset replacement patch, there are limitations to what can be achieved. Fixing the aforementioned issues would require decompiling the engine to manipulate UI and text element positioning, which is beyond the scope of this project. I've done as much as I could do with the tools that I was given.

## Screenshots

<p align="center">
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/.github/assets/SS1.png">
    <img src=".github/assets/SS1.png" alt="Main Menu" width="350"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/.github/assets/SS2.png">
    <img src=".github/assets/SS2.png" alt="In-game" width="350"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/.github/assets/SS3.png">
    <img src=".github/assets/SS3.png" alt="CGs" width="350"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/.github/assets/SS4.png">
    <img src=".github/assets/SS4.png" alt="Events" width="350"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/.github/assets/SS5.png">
    <img src=".github/assets/SS5.png" alt="Choices" width="350"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/.github/assets/SS6.png">
    <img src=".github/assets/SS6.png" alt="Battles" width="350"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/.github/assets/SS7.png">
    <img src=".github/assets/SS7.png" alt="Rankings" width="350"/>
  </a>
  <a href="https://raw.githubusercontent.com/Danar435/lbee-restoration/refs/heads/main/.github/assets/SS8.png">
    <img src=".github/assets/SS8.png" alt="Baseball" width="350"/>
  </a>
</p>

## Installing

Download the patch from the [releases tab](https://github.com/Danar435/lbee-restoration/releases)!

Afterwards, extract the zip file and copy its contents to the game installation directory, which is usually in `C:\Program Files (x86)\Steam\steamapps\common\Little Busters! English Edition`. When Windows prompts you about overwriting the files, click "Yes" to proceed. The patch is then installed!

Before installing the patch, consider backing up the `files` folder and `system.cnf` file to avoid redownloading the original files in case you want to revert the changes later. If you've already installed the patch and want to redownload the original files, right-click the game in Steam, select "Properties", navigate to "Installed Files", and click "Verify integrity of game files". Steam will then redownload all of the files that were replaced.

## Building

To build the patch on Linux, use the provided bash script. You'll need the [LuckSystem](http://github.com/wetor/LuckSystem/releases/latest/download/LuckSystem_linux_x86_64.zip) binary in the same folder as the script, or alternatively modify the script path as needed. 

To create the patch using the original uncensored assets, run:

```bash
./lbee-repack.sh /path/to/game/folder/
```

To create the patch using LBEE's censored assets, run:

```bash
./lbee-repack.sh -c /path/to/game/folder/
```


The script will repack the files and create an `output` folder containing the patched pak files. 

## Notes

I've made some notes for those looking into making a similar patch or contribute to this. You can [find them here](http://github.com/Danar435/lbee-restoration/blob/main/NOTES.md). If you have any questions regarding the process, then please use GitHub's Discussions instead of opening Issues.

## Special Thanks

- [WéΤοr](https://github.com/wetor) for [LuckSystem](https://github.com/wetor/LuckSystem) 
- [G2](https://github.com/G2-Games) for [lbee-utils](https://github.com/G2-Games/lbee-utils)
- [danil](https://github.com/thedanill) for [LB_repack](https://github.com/thedanill/LB_repack)
- [CPlusSharp](https://github.com/cplussharp/) for [GraphStudioNext](https://github.com/cplussharp/graph-studio-next)
- [Sep7](https://github.com/Sep7em) for feedback
- [Zipplet/Kotomi](https://github.com/zipplet)
