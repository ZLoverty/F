import os

folder = r"G:\My Drive\Research projects\F\Data"

sfL = next(os.walk(folder))[1]

for sf in sfL:
    ssfL = next(os.walk(os.path.join(folder, sf)))[1]
    for ssf in ssfL:
        if "early" in ssf:
            early_folder = os.path.join(folder, sf, ssf, "crop")
            # if os.path.exists(os.path.join(early_folder, "nrvf.h5")):
            #     print(f"{sf}/{ssf} Report already exists, skipping.")
            #     continue
            # else:
            #     print(f"Processing {sf}/{ssf}")
            os.system("python report_early.py \"{}\" -n 8 -o 0.3".format(early_folder))
        