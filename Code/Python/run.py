import os

main_folder = r"F:\F"
sfL = ["05282025"]
for sf in sfL:
    ssfL = next(os.walk(os.path.join(main_folder, sf)))[1]
    for ssf in ssfL:
        if "stack" in ssf:
            name = ssf.split("_")[0]
            folder = os.path.join(main_folder, sf, ssf)
            imgDir = os.path.join(folder, r"%04d.jpg")
            outDir = os.path.join(main_folder, sf, f"{name}.mp4")
            print(outDir)
            if not os.path.exists(outDir):
                print("converting")
                os.system(f"ffmpeg -framerate 25 -i {imgDir} {outDir}")