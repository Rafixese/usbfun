import ctypes
import os
import sys
from pathlib import Path


def set_wallpaper(image_path):
    # The SystemParametersInfo function signature
    SPI_SETDESKWALLPAPER = 20
    WALLPAPER_STYLE = 2  # Stretched style. Change it according to preference (0 for tiled, 6 for fit, 10 for fill, etc.)
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, WALLPAPER_STYLE)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        script_path = os.getcwd()
        wallpaper_rel_path = sys.argv[1]  # Get the wallpaper path from the first command line argument
        wallpaper_path = str(Path(script_path, wallpaper_rel_path))
        print("Setting wallpaper from", wallpaper_path)

        if os.path.isfile(wallpaper_path):
            set_wallpaper(wallpaper_path)
        else:
            print(f"File not found: {wallpaper_path}")
    else:
        print("Please provide the path to the wallpaper image as an argument.")
