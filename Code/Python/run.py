import os

folder = r"G:\My Drive\Research projects\F\Data\06282024\tracking\exp5\26-29"

params = {}
params["minThreshold"] = [0]
params["maxThreshold"] = [250]
params["circularity"] = [0.8]
params["convexity"] = [.5]
params["inertia"] = [.5]

cmd = f"python find_drops.py \"{folder}\""
for kw in params:
    for value in params[kw]:
        cmd += f" --{kw} {value}"
os.system(cmd)