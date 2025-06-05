import os
from pathlib import Path

main_folder = r"G:\My Drive\Research projects\F\Data"
for r, s, f in os.walk(main_folder):
    if "crop" in s:
        root = Path(r)
        folder = root / "crop"
        overlay_folder = folder / "overlay"
        if overlay_folder.exists():
            print(f"Skip {str(folder)}")
            continue
        else:
            print(f"Processing {str(folder)}")
            os.system(f"python overlay.py \"{str(folder)}\"")
            

