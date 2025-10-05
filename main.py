from gooey import Gooey, GooeyParser
from pathlib import Path
import os
import requests
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

    # Download any missing assets
    download(lucksystem, lucksystem_url)
    download(source, source_url)

    # Run the main repack script
    print("➡️ Patching main assets...")
    #for i in pak_list:
    #    repack(lucksystem, source, input, i)


    # Handle censoring assets
    if not args.censored:
        print("➡️ Patching uncensored assets...")
        #repack(lucksystem, Path(f"{source}/auxiliary-files/censored"), input, "eventcg")
        #repack(lucksystem, Path(f"{source}/auxiliary-files/censored"), input, "othcg")

    # Handle the Suginami mod
    if not args.suginami:
        print("➡️ Patching Suginami assets...")
        #repack(lucksystem, Path(f"{source}/auxiliary-files/suginami"), input, "charcg")
        #repack(lucksystem, Path(f"{source}/auxiliary-files/suginami"), input, "script")

    print("✅ Patching completed!")

def download(input, url):
    try:
        # Check if file exists
        input.resolve(strict=True)

    except:
        # Download via requests
        print(f"⬇️ Downloading {str(input).upper()}...")
        request = requests.get(url, allow_redirects=True)
        open(input.with_suffix('.zip'), 'wb').write(request.content)

        # Extract via zipfile
        with ZipFile(input.with_suffix('.zip'), 'r') as zObject:
            zObject.extract(input.name)
        os.remove(input.with_suffix('.zip'))
        os.chmod(input, 0o755)

    else:
        print(f"☑️ {str(input).upper()} already downloaded")

def repack(lucksystem, source, input, file):
    # Define paths
    pak = f"{file.upper()}.PAK"
    pak_input = Path(f"{source}/{file}-done/")
    pak_output = Path(f"{input}/files/{pak}-temp")
    pak_source = Path(f"{input}/files/{pak}")

    # Run lucksystem and replace original file
    print(f"ℹ️ Repacking {pak}...")
    os.system(f'./{lucksystem} pak replace \
              -s "{pak_source}" \
              -i "{pak_input}" \
              -o "{pak_output}"')
    os.rename(pak_output, pak_source)

if __name__ == '__main__':
    main()
