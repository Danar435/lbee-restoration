from gooey import Gooey, GooeyParser
from pathlib import Path
from zipfile import ZipFile
import os
import requests
import shutil
import subprocess
import sys

VERSION = "1.1.1"
SOURCE_SIZE = 2520

# Needed for Gnome to work properly
os.environ['GTK_THEME'] = 'Adwaita:light'

no_term = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0

# Determine image path
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)

# Handle arguments in GUI
@Gooey(
        default_size=(650, 500),
        program_name=f'LBEE Restoration Patch v{VERSION}',
        program_description="Restore the original look and feel of 'Little Busters English Edition'",
        show_restart_button=False,
        clear_before_run=True,
        image_dir=resource_path('assets/gooey'),
        progress_regex = r"(?P<progress>\d+)/(?P<total>\d+)",
        progress_expr="progress / total * 100"
        )
def main():
    # Define paths
    source = Path(f"./lbee-restoration-{VERSION}/source")
    source_url = f'https://github.com/Danar435/lbee-restoration/archive/refs/tags/v{VERSION}.zip'
    if os.name == 'nt':
        pakutil = Path(f"./lbee-restoration-{VERSION}/dependencies/pakutil-v0.2.1-a6-windows.exe")
        xdelta3 = Path(f"./lbee-restoration-{VERSION}/dependencies/xdelta3-v3.1.0-windows.exe")
    else:
        pakutil = Path(f"./lbee-restoration-{VERSION}/dependencies/pakutil-v0.2.1-a6-linux")
        xdelta3 = Path(f"./lbee-restoration-{VERSION}/dependencies/xdelta3-v3.1.0-linux")

    # List of paks to repack
    pak_list = [ "battle", "bgcg", "charcg", "eventcg", "gencg", "gm", 
                "othcg", "parts", "pt", "syscg", "script" ]
    uncensored_list = ["othcg", "eventcg", "script" ]
    suginami_list =  [ "script" ]

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
        print("[ERROR] LITBUS_WIN32.exe not found!", flush=True)
        print("Make sure that the game path is correct. It should point" \
        " to the folder 'Little Busters! English Edition'. Default installation path is" \
        " 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Little Busters! English Edition'", flush=True)
        sys.exit(1)

    # Set up progress variables
    progress = 0
    total = len(pak_list)
    if not args.uncensored:
        total += len(uncensored_list)
    if not args.suginami:
        total += len(suginami_list)

    # Download the source
    if not source.exists():
        print("Downloading the assets, this may take a few minutes...", flush=True)
        check_internet()
        with requests.get(source_url, stream=True) as r:
            r.raise_for_status()

            # GitHub doesn't provide `content-length`, must be set manually
            total_size = SOURCE_SIZE
            block_size = 8192
            downloaded = 0
            update = 0

            with open("source.zip", 'wb') as f:
                for chunk in r.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)/1024/1024
                        if downloaded >= update:
                            print(f"Downloading the assets: {int(downloaded)}/{total_size} MB", flush=True) 
                            update += 8

        # Extract via zipfile
        print("Extracting the assets...", flush=True)
        with ZipFile("source.zip", 'r') as zObject:
            zObject.extractall(".")
        os.remove("source.zip")
    else:
        print("The assets are already downloaded!", flush=True)

    # Make dependencies executable on linux
    if os.name != 'nt':
        os.chmod(pakutil, 0o755)
        os.chmod(xdelta3, 0o755)

    # Patch the exe
    print("Patching the executable...", flush=True)
    
    if not exe_backup.exists():
        shutil.copy(exe, exe_backup)

    # Hide console window on Windows
    exe_patch = subprocess.run([
                    os.path.join('.', xdelta3), "-d", "-f", "-s", 
                    exe_backup,
                    source / "auxiliary-files" / "LITBUS_WIN32.xdelta", 
                    exe
                    ], creationflags=no_term)
    
    if exe_patch.returncode != 0:
        print("[ERROR] Failed to patch the executable!", flush=True)
        print("Make sure that you are using a legitimate copy of LBEE. Any recent updates may break " \
        "the patch. If you have used this patch before and have deleted 'LITBUS_WIN32-backup.exe', " \
        "then please verify game files within Steam and run the patch again.", flush=True)
        sys.exit(1)

    # Patch the config
    print("Copying the config...", flush=True)
    shutil.copy(source / "auxiliary-files" / "system.cnf", input)

    # Patch the movies
    print("Copying the movies...", flush=True)
    shutil.copytree(source / "auxiliary-files" / "movie", input / "files" / "movie", dirs_exist_ok=True)

    # Run the main repack script
    print("Processing main assets...", flush=True)
    for i in pak_list:
        progress += 1
        repack(pakutil, source, input, i, progress, total)

    # Handle uncensoring assets
    if not args.uncensored:
        print("Processing uncensored assets...", flush=True)
        for i in uncensored_list:
            progress += 1
            repack(pakutil, source / "auxiliary-files" / "uncensored", input, i, progress, total)

    # Handle the Suginami mod
    if not args.suginami:
        print("Processing Suginami assets...", flush=True)
        for i in suginami_list:
            progress += 1
            repack(pakutil, source / "auxiliary-files" / "suginami", input, i, progress, total)

    # Remove overlays in characters pak
    print("Fixing CHARCG.PAK...", flush=True)
    with open(input / "files" / "CHARCG.PAK", "r+b") as file:
        file.seek(0x9568)
        file.write(b"\x00" * (0xA42C - 0x9568))

    # Remove decropper mod if present
    decropper_mod = input / "D3D11.dll"
    if decropper_mod.exists():
        print("Removing 'Decropper Mod'... (incompatible)", flush=True)
        os.remove(decropper_mod)

    # Finish
    print("[SUCCESS] Patching completed!", flush=True)

def check_internet():
    try:
        response = requests.get('https://www.google.com/', timeout=5)
        return
    except (requests.ConnectionError, requests.Timeout):
        print("[ERROR] Failed to connect to internet!", flush=True)
        print("If you want to use the installer offline, then download the source code separately " \
        "and extract it in the same folder as this patch. It should contain a folder named " \
        "'lbee-restoration-{VERSION}'.", flush=True)
        sys.exit(1)

def repack(pakutil, source, input, file, progress, total):
    # Define paths
    pak = f"{file.upper()}.PAK"
    pak_input = Path(f"{source}/{file}-done/")
    pak_output = Path(f"{input}/files/{pak}-temp")
    pak_source = Path(f"{input}/files/{pak}")

    # Error catching
    if not pak_source.exists():
        print(f"[ERROR] {pak} not found!", flush=True)
        print("Please verify game files within Steam and run the patch again.", flush=True)
        sys.exit(1)

    # Run pakutil and replace original file
    print(f"Repacking file {progress}/{total}: {pak}...", flush=True)
    subprocess.run([
        os.path.join('.', pakutil),
        pak_source,
        'replace', '-b',
        pak_input,
        pak_output
        ], creationflags=no_term)
    shutil.move(pak_output, pak_source)

if __name__ == '__main__':
    main()
