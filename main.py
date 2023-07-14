import os

mainDir = os.path.abspath (os.path.dirname (__file__))

import setup
setup.main (mainDir)

import json, sys, subprocess as sp, platform as pt
from PIL import Image


info_file_path = os.path.join (mainDir, "info.json")
settings_file_path = os.path.join (mainDir, "settings.json")
intersection_file_path = os.path.join (mainDir, "intersection.json")

img_dir = os.path.join (mainDir, "img")


def print_color_text(text: str, rgb: tuple [int, int, int] = (255, 255, 255)):
    return f"\033[38;2;{rgb [0]};{rgb [1]};{rgb [2]}m{text}\033[0m"


def get_info () -> dict:
    with open (info_file_path) as f:
        return json.load (f)
    

def get_flower_name () -> (str | None):
    try: return sys.argv [1].lower ()
    except IndexError: return get_def_flower ()


def get_def_flower () -> dict:
    OS = get_os_name ()

    with open (intersection_file_path) as f:
        x: dict = json.load (f)

        for key in x.keys ():
            if OS == key:
                return x [key]


def print_help () -> None:
    help = """Nothing ..."""
    print (help)
    exit ()


def get_flower_info (flower_name: str) -> (dict|None):
    info = get_info ()
    got: bool = False

    for value in info.values ():
        if flower_name == value ["FLOWER-NAME"].lower ():
            got = True
            return value
        
    if not got:
        print_error ("FlowerNotFoundError: Flower not found in the database.")
        exit ()


def print_error (error: str):
    print (f"\033[38;2;255;0;0;1m[-] {error}\033[0m")


def get_rgb (px_data: Image, index: tuple):
    return px_data [index]


def get_settings (section: str = False):
    with open (settings_file_path) as f:
        if section:
            return json.load (f)[section]
        
        else:
            return json.load (f)["App-Settings"]


def img2ascii (image_path: os.path = False):
    if not image_path:
        image_path = flower_info ["FLOWER-IMAGE-PATH"]

    ascii_chars = "@#%*+-. "

    img = Image.open(image_path)
    img = img.resize(image_settings ["resultant-dim"])

    ascii_image = []
    img_width, img_height = image_settings ["resultant-dim"][0], image_settings ["resultant-dim"][1]
    ascii_img_dim = ascii_settings ["img_aspect-ratio"]

    # Convert each pixel to ASCII character
    for i in range (0, img_height, img_height // ascii_img_dim [0]):
        x = []

        for j in range (0, img_width, img_width // ascii_img_dim [1]):
            pixel = img.getpixel ((j, i))[:3]
            if transparrent_bg: grayscale = (sum (pixel) // 3)
            else: grayscale = 255 - (sum (pixel) // 3)
            char_index = int (grayscale / 256 * len (ascii_chars))
            x.append (print_color_text (ascii_chars [char_index], pixel))

        ascii_image.append (x)

    return ascii_image


def get_os_name (full_data: bool = False) -> (str | list):
    ret = pt.platform ()
    neo_data = []

    try:
        # Run the neofetch command and capture the output
        output = sp.run (['neofetch', '--stdout'], capture_output = True, text = True).stdout.strip ()

        # Parse the output to find the OS name
        lines = output.split ('\n')

        for line in lines:
            neo_data.append (line)

            if line.startswith ('OS:'):
                ret = line [4:].strip ()

    except sp.CalledProcessError:
        pass

    if full_data:
        return neo_data
    
    else:
        # If neofetch command fails or the output doesn't contain OS name, fallback to platform module
        ret = ret.split (' ')
        RET = ''

        for i in ret:
            if i != ret [-1]:
                RET += i + ' '

        return RET [:-1]


def get_sys_details ():
    neofetch_data = get_os_name (True)
    new_data = {}

    for i in range (len (neofetch_data)):
        dat = neofetch_data [i]

        if i < 2:
            if '@' in dat:
                new_data ['Username'] = dat.split ('@')[0]
                new_data ['Hostname'] = dat.split ('@')[1]

        if ':' in dat:
            new_data [dat.split (':')[0]] = dat.split (':')[1][1:-1]

    print (json.dumps (new_data, indent = 4))


def integrate_info (ascii_image: list):
    keys = list (flower_info.keys ())

    to_be_added = [
        f"fulfetch@SRIJAN",
        f"---------------",
        f"{'Name'}: {flower_info ['FLOWER-NAME']}",
        f"{'Origin Country'}: {flower_info ['ORIGIN-COUNTRY']}",
        f"{'Blooming Season'}: {flower_info ['BLOOMING-SEASON']}",
        f"{'Symbolic Meaning'}: {flower_info ['SYMBOLIC-MEANING']}",
        f"{'Symbolic OS'}: {flower_info ['SYMBOLIC-OS']}",
        f"",
        f"",
        f"",
        f"",
        f"",
        f"",
        f"",
        f"",
        f"",
        f"",
        f"",
        f"",
        f"",
        f"",
        f"",
        f"",
        f""
    ]

    for i in range (len (ascii_image)):
            ascii_image [i].append (to_be_added [i])

    return ascii_image


def focused_mode (img_pth: os.path):
    
    ascii_img = img2ascii (img_pth)

    for i in range (len (ascii_img)):
        for j in range (len (ascii_img [i])):
            print (ascii_img [i][j], end = '')

        print ("\n", end = '')


def default_mode () -> None:
    global flower_info

    flower = get_flower_name ()
    flower_info = get_flower_info (flower)

    flower_info ["FLOWER-IMAGE-PATH"] = os.path.join (img_dir, flower_info ["FLOWER-IMAGE-PATH"])

    ascii_img = img2ascii ()
    #ascii_img = integrate_info (ascii_img)

    for i in range (len (ascii_img)):
        for j in range (len (ascii_img [i])):
            print (ascii_img [i][j], end = '')

        print ("\n", end = '')


def main () -> None:
    global image_settings, ascii_settings, transparrent_bg

    transparrent_bg = True

    image_settings = get_settings ("Image-Settings")
    ascii_settings = get_settings ("ASCII-Settings")

    if len (sys.argv) > 1:
        argv = sys.argv [1:]
        flags = []
        args = []

        for arg in argv:
            if arg [0] == '-': flags.append (arg.lower ().replace ('-', ''))
            else: args.append (arg)

        if len (flags) != 0:
            for flag in flags:
                if (flag == 'h') or (flag == 'help'): print_help ()
                if flag == 'nt': transparrent_bg = False
                if flag == 'f': focused_mode (args [0])

        else: default_mode ()

    else: default_mode ()


if __name__ == "__main__":
    main ()