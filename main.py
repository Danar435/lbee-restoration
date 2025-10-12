from gooey import Gooey, GooeyParser
from pathlib import Path
from zipfile import ZipFile
import os
import requests
import shutil
import subprocess

VERSION = "1.1.0"

# Needed for Gnome to work properly
os.environ['GTK_THEME'] = 'Adwaita:light'

# Handle arguments in GUI
@Gooey(
        default_size=(650, 500),
        program_name=f'LBEE Restoration Patch v{VERSION}',
        program_description="Restore the original look and feel of 'Little Busters English Edition'",
        show_restart_button=False,
        image_dir='assets/gooey',
        progress_regex=r"\((?P<progress>\d+)/(?P<total>\d+)\)$",
        progress_expr="progress / total * 100"
        )
def main():
    # Define paths
    source = Path(f"./lbee-restoration-{VERSION}/source")
    source_url = f'https://github.com/Danar435/lbee-restoration/archive/refs/tags/v{VERSION}.zip'
    if os.name == 'nt':
        lucksystem = Path(f"./lbee-restoration-{VERSION}/dependencies/lucksystem-windows.exe")
        xdelta3 = Path(f"./lbee-restoration-{VERSION}/dependencies/xdelta3-windows.exe")
    else:
        lucksystem = Path(f"./lbee-restoration-{VERSION}/dependencies/lucksystem-linux")
        xdelta3 = Path(f"./lbee-restoration-{VERSION}/dependencies/xdelta3-linux")

    # List of paks to repack
    pak_list = [ "battle", "bgcg", "charcg", "eventcg", "gencg", "gm", 
                "othcg", "parts", "pt", "syscg", "script" ]
    uncensored_list = ["othcg", "eventcg", "script" ]
    suginami_list =  ["charcg", "script" ]

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
    options.add_argument('-u', '--uncensored', 
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
    exe_backup = Path(f"{input}/LITBUS_WIN32-backup.exe")
    
    # Check if the path is right
    if not exe.exists():
        print("🟥 LITBUS_WIN32.exe not found!")
        print("ℹ️ Make sure that the game path is correct. " \
        "It should point to the folder 'Little Busters! English Edition'.")
        exit(1)

    # Set up progress variables
    progress = 0
    total = len(pak_list)
    if not args.uncensored:
        total += len(uncensored_list)
    if not args.suginami:
        total += len(suginami_list)

    # Download the source
    if not source.exists():
        # Download via requests
        print(f"⬇️ Downloading the assets...")
        check_internet()
        with requests.get(source_url, stream=True, allow_redirects=True) as r:
            r.raise_for_status()
            with open("source.zip", 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        # Extract via zipfile
        with ZipFile("source.zip", 'r') as zObject:
            zObject.extractall(".")
        os.remove("source.zip")
    else:
        print(f"☑️ The assets are already downloaded!")

    # Patch the exe
    print("ℹ️ Patching the executable...")
    
    if not exe_backup.exists():
        shutil.copy(exe, exe_backup)

    exe_patch = subprocess.run([
                    os.path.join('.', xdelta3), "-d", "-f", "-s", 
                    exe_backup,
                    source / "auxiliary-files" / "LITBUS_WIN32.xdelta", 
                    exe
                    ])
    
    if exe_patch.returncode != 0:
        print("🟥 Failed to patch the executable!")
        print("ℹ️ Make sure that you are using a legitimate copy of LBEE. Any recent updates may break " \
        "the patch. If you have used this patch before and have deleted 'LITBUS_WIN32-backup.exe', " \
        "then please verify game files within Steam and run the patch again.")
        exit(1)

    # Patch the config
    print("ℹ️ Patching the config...")
    shutil.copy(source / "auxiliary-files" / "system.cnf", input)

    # Patch the movies
    print("ℹ️ Patching the movies...")
    shutil.copytree(source / "auxiliary-files" / "movie", input / "files" / "movie", dirs_exist_ok=True)

    # Run the main repack script
    print("➡️ Patching main assets...")
    for i in pak_list:
        progress += 1
        repack(lucksystem, source, input, i, progress, total)

    # Handle uncensoring assets
    if not args.uncensored:
        print("➡️ Patching uncensored assets...")
        for i in uncensored_list:
            progress += 1
            repack(lucksystem, source / "auxiliary-files" / "uncensored", input, i, progress, total)

    # Handle the Suginami mod
    if not args.suginami:
        print("➡️ Patching Suginami assets...")
        for i in suginami_list:
            progress += 1
            repack(lucksystem, source / "auxiliary-files" / "suginami", input, i, progress, total)

    # Remove overlays in characters pak
    print("ℹ️ Fixing CHARCG.PAK...")
    with open(input / "files" / "CHARCG.PAK", "r+b") as file:
        file.seek(0x9568)
        file.write(b"\x00" * (0xA42C - 0x9568))

    # Remove decropper mod if present
    decropper_mod = input / "D3D11.dll"
    if decropper_mod.exists():
        print("ℹ️ Removing 'Decropper Mod'... (incompatible)")
        os.remove(decropper_mod)

    # Finish
    print("✅ Patching completed!")

def check_internet():
    try:
        response = requests.get('https://www.google.com/', timeout=5)
        return
    except (requests.ConnectionError, requests.Timeout):
        print("🟥 Failed to connect to internet!")
        print("ℹ️ If you want to use the installer offline, then download the source code and " \
            "lucksystem beforhand. Afterwards place the 'source' folder and 'LuckSystem_windows.exe' " \
            "or 'LuckSystem_linux' binary in the same folder as this patch.")
        exit(1)

def repack(lucksystem, source, input, file, progress, total):
    # Define paths
    pak = f"{file.upper()}.PAK"
    pak_input = Path(f"{source}/{file}-done/")
    pak_output = Path(f"{input}/files/{pak}-temp")
    pak_source = Path(f"{input}/files/{pak}")

    # Error catching
    if not pak_source.exists():
        print(f"🟥 {pak} not found!")
        print("ℹ️ Please verify game files within Steam and run the patch again.")
        exit(1)

    # Run lucksystem and replace original file
    print(f"ℹ️ Patching {pak}... ({progress}/{total})")

    # On windows
    if os.name == 'nt':
        for f in pak_input.iterdir():
            subprocess.run([
                os.path.join('.', lucksystem),
                'pak', 'replace',
                '-s', pak_source,
                '-i', pak_input / f.name,
                '-o', pak_output
            ])
            os.rename(pak_output, pak_source)

    # On linux
    else:
        subprocess.run([
            os.path.join('.', lucksystem),
            'pak', 'replace',
            '-s', pak_source,
            '-i', pak_input,
            '-o', pak_output
            ])
        os.rename(pak_output, pak_source)

    # windows not working, waiting for lbee-pakutil to support batch imports

if __name__ == '__main__':
    main()
