from PIL import Image
import os
import subprocess
from pathlib import Path
import sys
import struct

#   HELPER FILE

#   This file is meant to be modified to your needs. It is to be used as a shortcut for common tasks
#   The list of operations includes: `unpack`, `extract`, `import`, `repack`, `upscale`, `img-extract`, `img-overlay`
#   Do note that unpacking and repacking are only for bulk operations
#   It is a bit messy, but it gets the job done.

#   For bulk operations, use:          `python helper.py <pak> <operation> [<name>]`
#   For single file operations, use:   `python helper.py <operation> <input> <output> [<source>]`

#   Example of extracting characters cg
#   img-extract and img-overlay are used for images that have an overlay (so charcg and eventcg specifically)

#   Unpack a pak file:                  `python helper.py charcg unpack`
#   Extract all cz files in a pak:      `python helper.py charcg img-extract all`
#   Merge an overlay onto an image:     `python helper.py charcg img-overlay CGAY10 CGAY11`     (repeat for all overlays)
#   Restore overlay if used wrongly:    `python helper.py charcg img-extract CGAY12`
#   Upscale all extracted images:       `python helper.py charcg upscale scale960`              (upscales 2x and downscales to 960p)
#   Import all cz files in a pak:       `python helper.py charcg import`
#   Repack a pak file:                  `python helper.py charcg repack`

#   Example of editing a single image
#   You can also extract and import files at bulk (not recommended to import if images are different sizes)

#   Unpack a pak file:                  `python helper.py parts unpack`
#   Extract a single cz file:           `python helper.py extract ./workdir/parts-un/MWIN0 ./workdir/parts-ex/MWIN0.png`
#   Make changes to the png file...
#   Import a single cz file:            `python helper.py import ./workdir/parts-raw/MWIN0.png ./workdir/parts-done/MWIN0 ./workdir/parts-un/MWIN0`
#   Repack a pak file:                  `python helper.py parts repack`

#   Examples above are for Kanon, but it should work much the same way for LBEE


lucksystem = Path("./lucksystem")
pakdir = Path("backup/files/")
workdir = Path("workdir")
gamedir = Path("backup/Link to little-busters/files")

def ls_unpack(pak):

    output_dir = workdir / f"{pak}-un"
    output_dir.mkdir(exist_ok=True)
    pak = pakdir / f"{pak.upper()}.PAK"
    print(f"Unpacking {pak.name}...")
    
    try:
        subprocess.run([

        str(lucksystem),
        "pak", "extract",
        "-s", str(pak),
        "-i", str(pak),
        "-o", "out.txt",
        "-a", str(output_dir)

        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing {pak.name}: {e}")
        print(f"Command output: {e.stderr}")

    os.remove("out.txt")

def cz_single_extract(file_path, output_path):

    file_path = Path(file_path)
    print(f"Extracting {file_path.name}...")

    try:
        subprocess.run([
            
        "lbee-czutil",
        "decode",
        str(file_path),
        str(output_path)
        
        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing {file_path}: {e}")
        print(f"Command output: {e.stderr}")

def cz_extract(pak):

    input_dir = workdir / f"{pak}-un"
    output_dir = workdir / f"{pak}-ex"
    output_dir.mkdir(exist_ok=True)

    for i in input_dir.iterdir():
        cz_single_extract(input_dir / i.name, output_dir / f"{i.name}.png")

def cz_single_import(file_path, output_path, source_path=f"{workdir}/cg"):

    file_path = Path(file_path)
    print(f"Importing {file_path.name}...")

    try:
        result = subprocess.run([
        
        "lbee-czutil",
        "replace",
        str(source_path),
        str(file_path),
        str(output_path)
        
        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing {file_path.name}: {e}")
        print(f"Command output: {e.stderr}")

def cz_import(pak):

    input_dir = workdir / f"{pak}-raw"
    output_dir = workdir / f"{pak}-done"
    output_dir.mkdir(exist_ok=True)

    for i in input_dir.iterdir():
        cz_single_import(input_dir / i.name, output_dir / i.name.replace('.png', ''))

def ls_repack(pak):

    input_dir = workdir / f"{pak}-done"
    pak = pakdir / f"{pak.upper()}.PAK"
    print(f"Repacking {pak.name}...")

    try:
        subprocess.run([

        str(lucksystem),
        "pak", "replace",
        "-s", str(pak),
        "-i", str(input_dir),
        "-o", str(gamedir / pak.name),

        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing {pak.name}: {e}")
        print(f"Command output: {e.stderr}")

def w2_single_upscale(file_path, output_path, options=None):
    
    file_path = Path(file_path)
    print(f"Upscaling {file_path.name}...")

    try:
        result = subprocess.run([

        "waifu2x",
        "-s", "2",
        "-i", str(file_path),
        "-o", str(output_path)

        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing {file_path.name}: {e}")
        print(f"Command output: {e.stderr}")

    if options == "scale960":
        with Image.open(output_path) as img:
            img = img.resize((1280, 960), Image.LANCZOS)
            img.save(output_path)

def w2_upscale(pak):
    
    input_dir = workdir / f"{pak}-ex"
    output_dir = workdir / f"{pak}-raw"
    output_dir.mkdir(exist_ok=True)

    for i in input_dir.iterdir():
        w2_single_upscale(input_dir / i.name, output_dir / i.name, "scale960")

def img_single_extract(pak, name):

    bin = workdir / f"{pak}-un/{name}"
    img = workdir / f"{pak}-ex/{name}.png"
    print(f"Extracting {name}...")

    try:
        result = subprocess.run([

        "lbee-czutil",
        "decode",
        str(bin),
        str(img)

        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing {img}: {e}")
        print(f"Command output: {e.stderr}")

    with open(bin, 'rb') as binary:
        binary.seek(0x10)
        x_bytes = binary.read(2)
        y_bytes = binary.read(2)
        x = struct.unpack('<h', x_bytes)[0]
        y = struct.unpack('<h', y_bytes)[0]

    image = Image.open(img)
    coords = (1280, 960)
    match pak:
        case "charcg":
            coords = (960, 720)
        case "eventcg":
            coords = (1280, 960)
        case _:
            print(f"Unknown pak: {pak}, define coordinates.")
            return
    canvas = Image.new("RGBA", coords, color=(0, 0, 0, 0))
    canvas.paste(image, (x, y), image)
    canvas.save(img)

def img_extract(pak):

    input_dir = workdir / f"{pak}-un"
    output_dir = workdir / f"{pak}-ex"
    output_dir.mkdir(exist_ok=True)

    for i in input_dir.iterdir():
        img_single_extract(pak, i.name)

def img_single_overlay(pak, file_path, overlay_path):

    img = workdir / f"{pak}-ex/{file_path}.png"
    ovr = workdir / f"{pak}-ex/{overlay_path}.png"

    image = Image.open(img)
    overlay = Image.open(ovr)
    image.paste(overlay, (0, 0), overlay)

    image.save(ovr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Not enough arguments")
        sys.exit(1)

    match sys.argv[1:]:
        case [pak, "unpack"]:
            ls_unpack(pak)
        case [pak, "extract"]:
            cz_extract(pak)
        case [pak, "import"]:
            cz_import(pak)
        case [pak, "repack"]:
            ls_repack(pak)
        case [pak, "upscale"]:
            w2_upscale(pak)
        case [pak, "img-extract", "all"]:
            img_extract(pak)
        case [pak, "img-extract", name]:
            img_single_extract(pak, name)
        case [pak, "img-overlay", file_path, overlay_path]:
            img_single_overlay(pak, file_path, overlay_path)
        case ["extract", input_file, output_file]:
            cz_single_extract(input_file, output_file)
        case ["import", input_file, output_file]:
            cz_single_import(input_file, output_file)
        case ["import", input_file, output_file, source_path]:
            cz_single_import(input_file, output_file, source_path)
        case ["upscale", input_file, output_file]:
            w2_single_upscale(input_file, output_file)
        case ["upscale", input_file, output_file, options]:
            w2_single_upscale(input_file, output_file, options)
        case _:
            print("Unknown command")
            sys.exit(1)
    sys.exit(0)
