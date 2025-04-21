import os

folder = r"G:\My Drive\Research projects\F\Data"

sfL = next(os.walk(folder))[1]

for sf in sfL:
    ssfL = next(os.walk(os.path.join(folder, sf)))[1]
    for ssf in ssfL:
        if "early" in ssf:
            os.system("python report_early.py \"{}\" -n 8 -o 0.3".format(os.path.join(folder, sf, ssf, "crop")))
        