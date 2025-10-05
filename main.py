from gooey import Gooey, GooeyParser
from pathlib import Path
import os
import pyxdelta
import requests
import shutil
from zipfile import ZipFile

# Needed for Gnome to work properly
os.environ['GTK_THEME'] = 'Adwaita:light'

# Handle arguments in GUI
@Gooey(
        default_size=(650, 500),
        program_name='LBEE Restoration Patch',
        program_description="Restore the original look and feel of 'Little Busters English Edition'",
        show_restart_button=False,
        image_dir='assets')
def main():
    # Define variables (OS specific)
    if os.name == 'nt':
        lucksystem = Path("./LuckSystem_windows.exe")
        lucksystem_url = 'https://github.com/wetor/LuckSystem/releases/latest/download/LuckSystem_windows_x86_64.zip'
    else:
        lucksystem = Path("./LuckSystem_linux")
        lucksystem_url = 'http://github.com/wetor/LuckSystem/releases/latest/download/LuckSystem_linux_x86_64.zip'

    source = Path("./source")
    source_url = 'https://github.com/Danar435/lbee-restoration/archive/refs/tags/v1.0.2.zip'

    # List of paks to repack
    pak_list = [ "battle", "bgcg", "charcg", "eventcg", "gencg", "gm", "othcg", "parts", "pt", "syscg", "script" ]

    # Set up the parser
    parser = GooeyParser()

    # Required arguments
    required = parser.add_argument_group()
    required.add_argument('path', 
                          metavar='Game Path', 
                          help="The folder in which LBEE is installed", 
                          widget='DirChooser')

    # Optional arguments
    options = parser.add_argument_group("Optional Settings", gooey_options={'show_border': True})
    options.add_argument('-c', '--censored', 
                         metavar='Uncensored Assets', 
                         help="Use the original uncensored assets", 
                         action="store_false",
                         widget='BlockCheckbox', 
                         default=True,
                         gooey_options={'checkbox_label': ' Enable'})
    options.add_argument('-s', '--suginami', 
                         metavar='Suginami Mod', 
                         help="Include the fan-made Suginami mod", 
                         action="store_false",
                         widget='BlockCheckbox', 
                         default=True,
                         gooey_options={'checkbox_label': ' Enable'})

    args = parser.parse_args()
    input = Path(args.path)
    exe = Path(f"{input}/LITBUS_WIN32.exe")
    exe_backup = Path(f"{exe}-backup")

    # Error catching
    try:
        exe.resolve(strict=True)

    except:
        print("🟥 LITBUS_WIN32.exe not found!")
        print("Make sure that the game path is correct.")
        print("It should point to 'Little Busters! English Edition'.")
        exit(1)

    # Download any missing assets
    download(lucksystem, lucksystem_url)
    download(source, source_url)

    # Run the main repack script
    print("➡️ Patching main assets...")
    for i in pak_list:
        repack(lucksystem, source, input, i)

    # Handle uncensoring assets
    if not args.censored:
        print("➡️ Patching uncensored assets...")
        for i in ["othcg", "eventcg", "script" ]:
            repack(lucksystem, source / "auxiliary-files" / "uncensored", input, i)

    # Handle the Suginami mod
    if not args.suginami:
        print("➡️ Patching Suginami assets...")
        for i in ["charcg", "script"]:
            repack(lucksystem, source / "auxiliary-files" / "suginami", input, i)

    # Patch the exe
    print("ℹ️ Patching the executable...")
    try:
        exe_backup.resolve(strict=True)
    except:
        shutil.copy(exe, exe_backup)
        
    pyxdelta.decode(str(exe_backup), str(source / "auxiliary-files" / "LITBUS_WIN32.xdelta"), str(exe))

    # Patch the movies
    print("ℹ️ Patching the movies...")
    shutil.copytree(source / "auxiliary-files" / "movie", input / "files", dirs_exist_ok=True)

    # Patch the config
    print("ℹ️ Patching the config...")
    shutil.copy(source / "auxiliary-files" / "system.cnf", input)

    # Fix CHARCG.PAK
    print("ℹ️ Fixing CHARCG.PAK...")
    with open(input / "files" / "CHARCG.PAK", "r+b") as file:
        file.seek(0x9568)
        file.write(b"\x00" * (0xA42C - 0x9568))

    print("✅ Patching completed!")

def download(input, url):
    try:
        # Check if file exists
        input.resolve(strict=True)

    except:
        # Download via requests
        print(f"⬇️ Downloading {str(input).upper()}...")
        try:
            response = requests.get(url, allow_redirects=True)
            response.raise_for_status()
        except:
            print(f"🟥 Failed to download {url}.")
            print("If you want to use the installer offline, then download the source code and " \
                "lucksystem beforhand. Afterwards place the 'source' folder and 'LuckSystem_windows.exe' " \
                "or 'LuckSystem_linux' in the same folder as this patch")
            exit(1)
        open(input.with_suffix('.zip'), 'wb').write(response.content)

        # Extract via zipfile
        with ZipFile(input.with_suffix('.zip'), 'r') as zObject:
            zObject.extract(input.name)
        os.remove(input.with_suffix('.zip'))
        if os.name != 'nt':
            os.chmod(input, 0o755)

    else:
        print(f"☑️ {str(input).upper()} already downloaded")

def repack(lucksystem, source, input, file):
    # Define paths
    pak = f"{file.upper()}.PAK"
    pak_input = Path(f"{source}/{file}-done/")
    pak_output = Path(f"{input}/files/{pak}-temp")
    pak_source = Path(f"{input}/files/{pak}")

    # Error catching
    try:
        pak_source.resolve(strict=True)

    except:
        print(f"🟥 {pak} not found!")
        exit(1)

    # Run lucksystem and replace original file
    print(f"ℹ️ Repacking {pak}...")
    os.system(f'"{lucksystem}" pak replace \
              -s "{pak_source}" \
              -i "{pak_input}" \
              -o "{pak_output}"')
    os.rename(pak_output, pak_source)

if __name__ == '__main__':
    main()
